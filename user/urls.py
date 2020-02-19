from django.urls import path,include
from . import views
from django.conf.urls import url 

app_name = "user"

urlpatterns = [
    path('register/', views.register, name="register"),
    path('login/', views.login_request, name="login"),
    path('logout/', views.log_out, name="logout"),
    path('information/', views.information, name="information"),
    path('profile/', views.profile, name="profile"),
    path('recommend_friend/', views.recommend_friend, name="recommend_friend"),
    path('visit/<int:res_ID>', views.visit, name="visit"),
    path('review/<int:dish_id>/<int:res_ID>', views.review, name="review"),
    path('edit_review/<int:review_id>', views.edit_review, name="edit_review"),
]