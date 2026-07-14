from django.urls import path, include
from .views import CartViewSet, CartItemViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'carts', CartViewSet)
router.register(r'cart_items', CartItemViewSet)


urlpatterns = [
    path('', include(router.urls))
]