"""
URL configuration for crud project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tasks import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.sign_up, name='signup'),
    path('tasks/', views.tasks, name='tasks'),
    path('tasks-completed/', views.tasks_completed, name='tasks-completed'),
    path('logout/', views.sing_out, name='logout'),
    path('signin/', views.sign_in, name='signin'),
    path('tasks/create/', views.create_task, name='create-task'),
    path('tasks/<int:id>', views.task, name='task-detail'),
    path('tasks/<int:id>/complete', views.task_complete, name='task-complete'),
    path('tasks/<int:id>/delete', views.task_delete, name='task-delete'),
]
