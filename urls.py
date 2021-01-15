from django.urls import path
from likemovies import views

urlpatterns = [
    path('', views.likemovies_index, name='likemovies_index'),
    path('saveoption', views.watchedcontent_result, name='watchedcontent_result'),
    path('recommendations', views.recommendations_result, name='recommendations_result'),

]
