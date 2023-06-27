from django.urls import path
from . import views

app_name="Blog"

urlpatterns = [
    path('index/',views.home_page,name='home'),
    path('detail/<id>/',views.blog_detail_view,name="detail"),
    path('create/',views.create_view,name='create'),
    path('update/<id>/',views.update_view,name='update'),
    path('delete/<id>/',views.delete_view,name='delete'),
    path('like/<id>/',views.like_blog,name='like_blog'),
     
]
