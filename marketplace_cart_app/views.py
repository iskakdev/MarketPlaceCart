from .serializers import CartSerializers, CartItemSerializers
from rest_framework import viewsets
from .models import Cart, CartItem


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializers

    def perform_create(self, serializer):
        serializer.save(user=self.request.user.id)


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializers