from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
 
 #===========================User Urls====================================
 
    path('',views.loginuser,name='login-user'),
    path('signup/',views.signup_user,name='signup'),
    path('suggest-password/',views.suggest_password,name='suggest-password'),
    path('add-new-blog/<int:id>',views.create_blog, name='add-new-blog'),
    path('view-blog/',views.view_blogs,name='view-blog'),
    path('add-comment/<int:id>/<int:user_id>',views.post_comments,name='add-comment'),
    path('view-comment/<int:id>',views.get_comment,name= 'get-comment'),
    path('view-my-blog/<int:id>',views.my_blogs,name='view-my-blog'),
    path('edit-blog/<int:id>',views.edit_blog, name='edit-blog'),
    path('delete-blog/<int:id>',views.delete_blog,name='delete-blog'),
    path('user-details/<int:id>/',views.get_user,name='user-details'),

]
