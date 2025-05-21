from django.shortcuts import render, get_object_or_404, redirect
from .models import Memo, Tag
from .utils import get_cached_constants

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

def memo_detail(request, pk):
    memo = get_object_or_404(Memo, pk=pk)
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

def memo_edit(request, pk):
    memo = get_object_or_404(Memo, pk=pk)
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

def memo_delete(request, pk):
    memo = get_object_or_404(Memo, pk=pk)
    if request.method == 'POST':
        memo.delete()
        return redirect('memo_list')
    return render(request, 'memo/memo_confirm_delete.html', {'memo': memo})


def some_view(request):
    # 特定カテゴリの定数を取得
    type1_constants = get_cached_constants('type1')

    # 取得した定数の処理
    for constant in type1_constants:
        print(f"{constant.phrase}: {constant.remark}")

    context = {
        'constants': type1_constants,
        # その他のコンテキスト変数
    }

    return render(request, 'memo/template.html', context)
