from django.shortcuts import render, get_object_or_404, redirect
from .models import Memo, Tag, Project, Task, Milestone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

def memo_list(request):
    tag_id = request.GET.get('tag')
    sidebar_tags = Tag.objects.all()
    if tag_id == "None":
        memos = Memo.objects.filter(tag__isnull=True)
    elif tag_id:
        memos = Memo.objects.filter(tag_id=tag_id)
    else:
        memos = Memo.objects.all()
    return render(request, 'memo/memo_list.html', {
        'memos': memos,
        'sidebar_tags': sidebar_tags,
        'selected_tag_id': tag_id,
    })

def memo_detail(request, memo_id):
    memo = get_object_or_404(Memo, pk=memo_id)
    sidebar_tags = Tag.objects.all()
    return render(request, 'memo/memo_detail.html', {
        'memo': memo,
        'sidebar_tags': sidebar_tags,
    })

def memo_create(request):
    tags = Tag.objects.all()
    sidebar_tags = Tag.objects.all()
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        tag_id = request.POST.get('tag')
        new_tag_name = request.POST.get('new_tag')
        tag = None
        new_tag = None
        if tag_id == '__new__' and new_tag_name:
            tag, _ = Tag.objects.get_or_create(name=new_tag_name)
            new_tag = new_tag_name
        elif tag_id:
            tag = Tag.objects.get(id=tag_id)
        memo = Memo.objects.create(title=title, content=content, tag=tag)
        return redirect('memo_list')
    return render(request, 'memo/memo_form.html', {
        'tags': tags,
        'sidebar_tags': sidebar_tags,
    })

def memo_update(request, memo_id):
    memo = get_object_or_404(Memo, pk=memo_id)
    tags = Tag.objects.all()
    sidebar_tags = Tag.objects.all()
    new_tag = None
    if request.method == 'POST':
        memo.title = request.POST['title']
        memo.content = request.POST['content']
        tag_id = request.POST.get('tag')
        new_tag_name = request.POST.get('new_tag')
        if tag_id == '__new__' and new_tag_name:
            tag, _ = Tag.objects.get_or_create(name=new_tag_name)
            memo.tag = tag
            new_tag = new_tag_name
        elif tag_id:
            memo.tag = Tag.objects.get(id=tag_id)
        else:
            memo.tag = None
        memo.save()
        return redirect('memo_list')
    return render(request, 'memo/memo_form.html', {
        'memo': memo,
        'tags': tags,
        'sidebar_tags': sidebar_tags,
        'new_tag': new_tag,
    })

def memo_delete(request, memo_id):
    memo = get_object_or_404(Memo, pk=memo_id)
    if request.method == 'POST':
        memo.delete()
        return redirect('memo_list')
    return render(request, 'memo/memo_confirm_delete.html', {'memo': memo})

@login_required
def project_list(request):
    projects = Project.objects.filter(user=request.user)
    return render(request, 'memo/project_list.html', {'projects': projects})

@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)
    tasks = project.tasks.all()
    milestones = project.milestones.all()
    return render(request, 'memo/project_detail.html', {
        'project': project,
        'tasks': tasks,
        'milestones': milestones
    })

@login_required
def project_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        
        project = Project.objects.create(
            name=name,
            description=description,
            start_date=start_date,
            end_date=end_date,
            user=request.user
        )
        messages.success(request, 'プロジェクトを作成しました。')
        return redirect('project_detail', project_id=project.id)
    
    return render(request, 'memo/project_form.html')

@login_required
def task_create(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        status = request.POST.get('status')
        priority = request.POST.get('priority')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        assigned_to_id = request.POST.get('assigned_to')
        
        task = Task.objects.create(
            title=title,
            description=description,
            project=project,
            status=status,
            priority=priority,
            start_date=start_date,
            end_date=end_date,
            assigned_to_id=assigned_to_id
        )
        messages.success(request, 'タスクを作成しました。')
        return redirect('project_detail', project_id=project.id)
    
    return render(request, 'memo/task_form.html', {'project': project})

@login_required
def task_update(request, task_id):
    task = get_object_or_404(Task, id=task_id, project__user=request.user)
    
    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.status = request.POST.get('status')
        task.priority = request.POST.get('priority')
        task.start_date = request.POST.get('start_date')
        task.end_date = request.POST.get('end_date')
        task.assigned_to_id = request.POST.get('assigned_to')
        task.save()
        
        messages.success(request, 'タスクを更新しました。')
        return redirect('project_detail', project_id=task.project.id)
    
    return render(request, 'memo/task_form.html', {'task': task})

@login_required
def gantt_chart(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)
    tasks = project.tasks.all()
    milestones = project.milestones.all()
    
    return render(request, 'memo/gantt_chart.html', {
        'project': project,
        'tasks': tasks,
        'milestones': milestones
    })

@login_required
def task_edit(request, project_id, task_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)
    task = get_object_or_404(Task, id=task_id, project=project)
    
    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.start_date = request.POST.get('start_date')
        task.end_date = request.POST.get('end_date')
        task.status = request.POST.get('status')
        task.priority = request.POST.get('priority')
        milestone_id = request.POST.get('milestone')
        if milestone_id:
            task.milestone = get_object_or_404(Milestone, id=milestone_id, project=project)
        else:
            task.milestone = None
        task.save()
        messages.success(request, 'タスクを更新しました。')
        return redirect('project_detail', project_id=project.id)
    
    milestones = Milestone.objects.filter(project=project)
    return render(request, 'memo/task_form.html', {
        'project': project,
        'task': task,
        'milestones': milestones
    })

@login_required
def task_detail(request, project_id, task_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)
    task = get_object_or_404(Task, id=task_id, project=project)
    milestones = Milestone.objects.filter(project=project)
    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.start_date = request.POST.get('start_date')
        task.end_date = request.POST.get('end_date')
        task.status = request.POST.get('status')
        task.priority = request.POST.get('priority')
        milestone_id = request.POST.get('milestone')
        if milestone_id:
            task.milestone = get_object_or_404(Milestone, id=milestone_id, project=project)
        else:
            task.milestone = None
        task.save()
        messages.success(request, 'タスクを更新しました。')
        return redirect('project_detail', project_id=project.id)
    return render(request, 'memo/task_detail.html', {
        'project': project,
        'task': task,
        'milestones': milestones
    })

@login_required
def task_delete(request, project_id, task_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)
    task = get_object_or_404(Task, id=task_id, project=project)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'タスクを削除しました。')
        return redirect('project_detail', project_id=project.id)
    return redirect('task_detail', project_id=project.id, task_id=task.id)
