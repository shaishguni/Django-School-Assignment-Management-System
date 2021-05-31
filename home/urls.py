from django.urls import path
from home import views
urlpatterns = [
    path('home/', views.dashboard, name="home"),

    path('assignments/create/', views.create_assignment, name='add_assignment'),
    path('assignments/<id>/pass', views.pre_submission,
        name='pre_submission'),

    path('assignments/<id>/', views.assignment_detail),

    path('submissions/', views.all_submmission, name="all_submmission"),


    path('assignments/<id>/detail/', views.assignments_detail, name="assignments_detail"),

    path('assignments/', views.all_assignment, name='all_assignment'),

    path('submissions/all/', views.all_assignment_submmission, name='all_assignment_submmission'),

	path('assignments/<id>/delete', views.delete_assignment,
        name='delete_assignment'),

    path('assignments/<id>/edit', views.edit_assignment,
        name='edit_assignment'),

    path('assignments/<id>/submission/', views.submit_assignment,
        name='assignment_submission'),

    path('submissions/<id>/delete', views.delete_submission,
        name='delete_submission'),

    path('submissions/<id>/edit', views.edit_submission,
        name='submission_detail'),


    path('assignments/<id>/submissions', views.assignment_submissions,
        name='submissions'),

    path('assouncement/add/', views.create_Notification),
    path('notifications/', views.all_notification),
    path('test/', views.test)
    # path('notifications/clear/', views.clear_notifications),
]
