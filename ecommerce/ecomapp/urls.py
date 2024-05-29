from django.urls import path,include
from django.conf.urls.static import static
from ecomapp import views
from django.conf import settings

urlpatterns = [
    path('',views.index),
    path('about/',views.about),
    path('contact/',views.contact),
    path('cart/',views.cart),
    path('login/',views.user_login),
    path('register/',views.register),
    path('logout/',views.user_logout),
    path('catfilter/<a>',views.cat_filter),
    path('sort/<b>',views.sort),
    path('range/',views.range1),
    path('pdetails/<pid>',views.productsdetails),
    path('addtocart/<pid>',views.addtocart),
    path('remove/<cid>',views.remove),
    path('qty/<a>/<pid>',views.cartqty),
    path('placeorder/',views.placeorder)
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)