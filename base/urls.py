from django.urls import path
from . import views
from django.http import HttpResponse

def test2(request):
    return HttpResponse("test-2")




urlpatterns = [
    path('',views.home,name="home"),
    path('loginpage/',views.loginpage,name="login"),  
    path('logoutpage/',views.logoutpage,name="logout"),  
    path('registerpage/',views.registerpage,name="register"),  
    path('test2/',test2),
    path('room/<str:pk>/',views.room,name="room"),
    path('profile/<str:pk>/',views.userprofile,name="profile"),
    path('createform/',views.createform,name="createform"),
    path('updateform/<str:pk>/',views.update,name="updateform"),
    path('deleteform/<str:pk>/',views.delete,name="deleteform"),
    path('deletemessage/<str:pk>/',views.deletemessage,name="delete-message"),
    path('updateuser/',views.updateuser,name="update-user"),
    path('topics/',views.topicspage,name="topics"),
    path('activity/',views.activitypage,name="activity"),
]