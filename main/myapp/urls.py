from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.TaskList.as_view(), name='task_list'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('register/', views.RegisterPage.as_view(), name='register'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('task-create/', views.TaskCreate.as_view(), name='task-create'),
    path('task-update/<int:pk>/', views.TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<int:pk>/', views.DeleteView.as_view(), name='task-delete'),
    path('completed/', views.completed_tasks, name='completed_tasks'),
    path('pending/', views.pending_tasks, name='pending_tasks')
]