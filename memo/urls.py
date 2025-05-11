from django.urls import path
from . import views

urlpatterns = [
    path('', views.memo_list, name='memo_list'),
    path('memo/<int:memo_id>/', views.memo_detail, name='memo_detail'),
    path('memo/new/', views.memo_create, name='memo_create'),
    path('memo/<int:memo_id>/edit/', views.memo_update, name='memo_update'),
    path('memo/<int:memo_id>/delete/', views.memo_delete, name='memo_delete'),
    
    # タスク管理のURL
    path('projects/', views.project_list, name='project_list'),
    path('projects/<int:project_id>/', views.project_detail, name='project_detail'),
    path('projects/new/', views.project_create, name='project_create'),
    path('projects/<int:project_id>/tasks/new/', views.task_create, name='task_create'),
    path('projects/<int:project_id>/tasks/<int:task_id>/edit/', views.task_edit, name='task_edit'),
    path('projects/<int:project_id>/gantt/', views.gantt_chart, name='gantt_chart'),
    path('projects/<int:project_id>/tasks/<int:task_id>/', views.task_detail, name='task_detail'),
    path('projects/<int:project_id>/tasks/<int:task_id>/delete/', views.task_delete, name='task_delete'),
]