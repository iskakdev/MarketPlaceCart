from django.db import models

class Cart(models.Model):
    user = models.IntegerField()
    

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.IntegerField()
    quantity = models.PositiveIntegerField()
