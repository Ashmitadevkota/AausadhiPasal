from django.urls import path, include
from. import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    # path('register/',views.registerFunction,name="register"),
   path('reg/', views.SignUp_function, name='reg'),
   path('login/', views.Login_function, name='login'),  
   path('verify/',views.verifyUser,name="verify"),
   path("logout/", auth_views.LogoutView.as_view(next_page='/'), name="logout"),
   path('changepass/',views.ChangePassword,name='changepass'),


]
