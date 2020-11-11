from django.urls import path     
from . import views
urlpatterns = [
    path('', views.index),
       path('register', views.register),
        path('success', views.success),
        path('log', views.log),
        path('logout', views.logout),
        path('addmessage', views.addmessage),
        path('addcomment/<str:id>', views.addcomment),

]
