from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from myapp import views

urlpatterns = [
    path('',views.index,name='index'),
    path('calendar',views.calender,name='calender'),
    path('entry/<int:pk>',views.details,name='details'),
    path('entry/add',views.add,name='add'),
    path('entry/delete/<int:pk>',views.delete,name='delete'),
    path('admin/', admin.site.urls),
    path('logout/',auth_views.logout,{'next_page': '/'},name='logout'),
    
    path('login/',auth_views.login,name='login'),
    path('signup/',views.signup,name='signup'),
    
]
