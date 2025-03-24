from django.urls import path
from .views import *

urlpatterns = [
    path('', quiz_list, name='quiz_list'),
    path('<int:pk>/', quiz_detail, name='quiz_detail'),
    path('signup/', signup, name='signup'),
    path('create-quiz/', create_quiz, name='create_quiz'),
    path('contact/', contact_view, name='contact'),
    path('my-quizzes/', my_quizzes, name='my_quizzes'),
    path('quizzes/', quiz_search, name='quiz_search'),
]