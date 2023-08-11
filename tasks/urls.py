from django.urls import path
from tasks import views

urlpatterns = [
    path("",views.home, name="home"),
    path("signup/",views.signup, name="signup"),
    path("tasks/",views.tasks, name="tasks"),
    path("logout/",views.signout, name="logout"),
    path("signin/",views.signin, name="signin"),
    path("tasks/create/",views.create_task, name="create_task"),
    path("tasks/<str:id>/",views.task_detail, name="task_detail"),
    path("tasks/update/<str:id>/",views.update_task, name="update_task"),
    path("tasks/delete/<str:id>/",views.delete_task, name="delete_task"),
    path("tasks/completed/<str:id>/",views.task_completed, name="task_completed"),
    path("tasks/performed",views.all_tasks_performed, name="all_tasks_performed"),
]