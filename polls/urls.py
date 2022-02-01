from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_question_database', views.add_question_database),
    path('add_question_redis', views.add_question_redis),
    path('add_question_sqs', views.add_question_sqs),
    path('add_question_dynamo', views.add_question_dynamo),
]
