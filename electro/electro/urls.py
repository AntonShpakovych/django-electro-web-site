from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.urls.conf import include
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('shop.urls', 'shop'), namespace='shop')),
    path('cart/', include(('cart.urls', 'cart'), namespace='cart')),
    path('myauth/', include(('myauth.urls', 'myauth'), namespace='myauth')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
