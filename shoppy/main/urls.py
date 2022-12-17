from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static 

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('homepage', views.homepage, name='homepage'),
    path('categories', views.categories, name='categories'),
    path('browse', views.browse, name='browse'),
    path('categoryitems/<int:category_id>', views.categoryitems, name='categoryitems'),
    path('item/<str:slug>/<int:id>', views.itempage, name='itempage'),
    path('search', views.search, name='search'),
    path('filter-data', views.filter_data, name='filter_data'),
    path('cart', views.cart, name='cart'),
    path('addtocart', views.addtocart, name='addtocart'),
    path('deletefromcart', views.deletefromcart, name='deletefromcart'),
    path('updatecart', views.updatecart, name='updatecart'),
    path('checkout', views.checkout, name='checkout'),
    path('ordersuccessful', views.ordersuccessful, name='ordersuccessful'),
    path('accounts/register', views.register, name='register'),
    path('registersuccessful', views.registersuccessful, name='registersuccessful'),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('paymentsuccessful/', views.paymentsuccessful, name='paymentsuccessful'),
    path('paymentcancelled/', views.paymentcancelled, name='paymentcancelled'),
    path('account', views.account, name='account'),
    path('orders', views.orders, name='orders'),
    path('orderitems/<int:id>', views.orderitems, name='orderitems'),
    path('userdetails', views.userdetails, name='userdetails'),
]

if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
