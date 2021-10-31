from . import views
from django.urls import path


urlpatterns = [
    path('login/', views.log_in, name='login'),
    path('logout/', views.log_out, name='logout'),
    path('signin/', views.sign_in, name='signin'),
    path('user_page/<user_id>/', views.user_page, name='user_page'),
    path('admin_page/', views.my_admin_only_view, name='admin_page'),
    path('admin_change_order/<order_id>',
         views.change_order, name='admin_change_order')
]
