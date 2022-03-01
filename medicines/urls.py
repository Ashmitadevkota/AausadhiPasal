from medicines import views
from django.urls import path

urlpatterns = [
    path('', views.index_page, name="home"),
    path('store/',views.store,name="store"),
    path('cart/',views.cart,name="cart"),
    path('checkout/',views.checkout,name="checkout"),
    path('product/',views.prod_detail,name="product"),
    path('product/<int:id>/',views.prod_detail,name="product"),
    path('update_item/',views.updateItem,name="update_item"),


    
]
