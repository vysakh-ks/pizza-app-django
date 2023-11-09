from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home,name="home"),
    path('menu/',views.menu,name="menu"),
    path('home/',views.home,name="home"),
    path('signup/',views.signup,name="signup"),
    path('login_data/',views.login_data,name="login_data"),
    path('orders/',views.orders,name="orders"),
    path('increament/',views.increament,name="increament"),
    path('decreament/',views.decreament,name="decreament"),
    path('deleteOrder/',views.deleteOrder,name="deleteOrder"),
    path('deleteallOrders/',views.deleteallOrders,name="deleteallOrders"),
    path('orderConfirmed/',views.orderConfirmed,name="orderConfirmed"),
    path('profile/',views.profile,name="profile"),
    path('address/',views.address,name="address"),
    path('logout_user/',views.logout_user,name="logout_user"),
    path('contact/',views.contact,name="contact"),

    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)