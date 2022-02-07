from medicines import views
from django.urls import path

urlpatterns = [
    path('', views.index_page, name="home"),
    
]
