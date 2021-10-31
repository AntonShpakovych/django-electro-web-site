from collections import namedtuple
from django.urls import path
from shop import views


urlpatterns = [
    path('', views.home_page, name='home'),
    path('store/', views.store_page, name='store'),
    path('store/<category_slug>/',
         views.store_list_categories, name='categories_list'),
    path('product/<id>/<slug>/', views.product_page, name='product'),
    path('checkout/', views.checkout_page, name='checkout'),
    # path('order_create/', views.order_create, name='order_create')
]
