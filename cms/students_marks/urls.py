from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('home/', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('add/', views.add_student_view, name='add_student'),
    path('edit/<int:student_id>/', views.edit_marks_view, name='edit_marks'),
    path('delete/<int:student_id>/', views.delete_student_view, name='delete_student'),
    path('logout/', views.logout_view, name='logout'),

    path("audit-log/", views.audit_log_view, name="audit_log"),
]
