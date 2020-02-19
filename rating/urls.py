from django.urls import path,include
from django.conf.urls import url 
from . import views

app_name = "rating"

urlpatterns = [
    path('index', views.index, name='index'),
    path('',views.homepage, name='homepage'), #a homepage function

    path('detail/<int:res_ID>/', views.detail, name='detail'), 
    path('delete/<int:res_ID>', views.destroy, name='delete'),
    path('edit/<int:res_ID>', views.edit, name='edit'),
    path('update/<int:res_ID>', views.update, name='update'), 
    path('insert', views.insert, name='insert'),
    path('res', views.res, name='res'), 
    path('search', views.search, name='search'), 
    path('recommend', views.recommend, name='recommend'),
    path('advanceSearch', views.advanceSearch, name='advanceSearch'), 
    path('ranking', views.ranking, name='ranking'), 
    path('person_rank', views.person_rank, name='person_rank'), 

]
