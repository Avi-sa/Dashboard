from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home,name="Dashboard"),
    path('products/',views.product,name="product"),
    path('orders/',views.orders,name="orders"),
    path('customer/<str:id>/',views.customer,name="customer"),
    path('create_order/<str:pk>',views.createOrder,name="create_order"),
    path('update_order/<str:pk>/',views.updateForm,name="update_order"),
    path('delete_order/<str:pk>/',views.delete_form,name="delete_form"),
    path('login/',views.loginview,name='login'),
    path('register/',views.register,name='register'),
    path('logout/',views.logoutuser,name='logout'),
    path('user/',views.UserPage,name='user'),
    path('settings/',views.account_settings,name='account_settings'),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
