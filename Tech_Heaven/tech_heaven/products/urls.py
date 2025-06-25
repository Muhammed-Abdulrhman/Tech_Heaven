# urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('', home_view, name='home'),
    path('category/<str:category_name>/', category_view, name='category'),
    path('product/<int:product_id>/', product_view, name='product'),
    path('cart/', cart_view, name='cart'),
    path('cart/delete/<int:cart_id>/', delete_cart_item, name='delete_cart_item'),
]