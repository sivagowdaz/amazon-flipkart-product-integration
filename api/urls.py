from django.urls import path
from . views import product_fun

urlpatterns = [
    path('afproducts/', product_fun, name='afproducts' )
]