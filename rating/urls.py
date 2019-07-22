from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('detail/<int:res_ID>/', views.detail, name='detail'), 
    path('delete/<int:res_ID>', views.destroy, name='delete'),
    path('edit/<int:res_ID>', views.edit, name='edit'),
    path('update/<int:res_ID>', views.update, name='update'), 
    path('insert', views.insert, name='insert'),
    path('res', views.res, name='res'), 
    path('search', views.search, name='search'), 
    path('result', views.searchResult, name='result'), 
    path('recommend', views.recommend, name='recommend'),
    path('price_re', views.price_re, name='price_re'), 

]
