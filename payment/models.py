from django.db import models
from django.contrib.auth.models import User
from app.models import Product

# Create your models here.


class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    shipping_full_name = models.CharField(max_length=255)
    shipping_email = models.CharField(max_length=255)
    shipping_address1 = models.CharField(max_length=255)
    shipping_address2 = models.CharField(max_length=255)
    shipping_city = models.CharField(max_length=255)
    shipping_state = models.CharField(max_length=255, null=True, blank=True)
    shipping_zipcode = models.CharField(max_length=255, null=True, blank=True)
    shipping_country = models.CharField(max_length=255)
    
    #don't pluralize address
    class Meta:
        verbose_name_plural = "Shipping Address"
        
    def __str__(self):
        return f'Shipping Address - {str(self.id)}'
    
    #create order model
    class Order(models.Model):
        #foreign key
        user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
        full_name = models.CharField(max_length=250)
        email = models.EmailField(max_length=250)
        shipping_address = models.CharField(max_length=15000)
        amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
        date_ordered = models.DateTimeField(auto_now_add=True)
        
        def __str__(self):
            return f'Order - {str(self.id)}'
        
    
    
    #create order item model
    