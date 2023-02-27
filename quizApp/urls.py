from django.urls import path
from django.contrib import admin
from . import views
from .views import home, register, login_view, logout_view


urlpatterns = [
    path('', views.home, name='home'),
    # auth urls
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register, name='register'),
    # share quiz
    path('share/<int:quiz_id>',views.share_quiz, name="share_quiz"),
    path('shared-with-me/',views.shared_with_me, name="shared_with_me"),

    path('CreateQuiz/', views.create_quiz, name='CreateQuiz'),
    path('quiz_list/', views.quiz_list, name='quiz_list'),
    path('view_quiz/<int:quiz_id>/', views.view_quiz, name='view_quiz'),
    path('delete_quiz/<int:quiz_id>/', views.delete_quiz, name='delete_quiz'),
    path('search/', views.quiz_search, name='quiz_search'),
    # questions functionalites 
    path('add_questions/<int:quiz_id>/', views.add_questions, name="add_questions"),
    path('update_questions/<int:question_id>/',views.update_question, name="update_question"),
    path('delete_question/<int:question_id>/',views.delete_question, name="delete_question"),
    # quiz launch and score Functionalites
    path('launch_quiz/<int:quiz_id>/',views.launch_quiz, name="launch_quiz"),
    path('submit_quiz/<int:quiz_id>/',views.submit_quiz, name="submit_quiz"),
]
