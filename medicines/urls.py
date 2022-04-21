from numpy import delete
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
    path('remove_cart/<int:id>/',views.remove_from_cart,name="remove_cart"),
    path('remove_wishlist/<int:id>/',views.remove_from_wishlist,name="remove_wishlist"),
    path('process_order/',views.ProcessOrder,name='process_order'),
    path('search/', views.searchBar, name = 'search'),
    path('wishlist',views.wishlist, name="wishlist"),
    path('add-to-wishlist',views.addtowishlist, name = "addtowishlist"),
    path('api/khalti_payment',views.khalti,name='verify_payment'),
    path('profile/',views.profile,name="profile"),
    path('about/',views.about,name="about"),
    
]
