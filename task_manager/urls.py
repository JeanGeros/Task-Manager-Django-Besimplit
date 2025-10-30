from django.urls import path
from . import views

app_name = 'task_manager'

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('tasks/create-modal/', views.task_create_modal, name='task_create_modal'),
    path('tasks/create/', views.task_create, name='task_create'),
    path('tasks/<int:pk>/', views.task_detail, name='task_detail'),
    path('tasks/<int:pk>/update/', views.task_update, name='task_update'),
    path('tasks/<int:pk>/toggle/', views.task_toggle, name='task_toggle'),
    path('tasks/<int:pk>/delete/', views.task_delete, name='task_delete'),
    path('export/csv/', views.export_tasks_report, name='export_csv'),
    path('export/excel/', views.export_tasks_excel, name='export_excel'),
]
