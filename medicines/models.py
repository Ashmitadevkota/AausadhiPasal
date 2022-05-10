import email
from enum import Flag
from pickle import TRUE
from pickletools import read_uint1
from pyexpat import model
from statistics import mode
from sys import maxsize
from urllib.request import urlcleanup
from xmlrpc.client import TRANSPORT_ERROR
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from jinja2 import ModuleLoader
from numpy import maximum
from zmq import DEALER


# Create your models here.



ORDER_STATUS = (
    ("Order Received", "Order Received"),
    ("Order Processing", "Order Processing"),
    ("On the way", "On the way"),
    ("Order Completed", "Order Completed"),
    ("Order Canceled", "Order Canceled"),
)

METHOD = (
    ("Cash On Delivery", "Cash On Delivery"),
    ("Khalti Pay", "Khalti Pay"),
    
)

# class Customer(models.Model):
#     # user = models.OneToOneField(User,on_delete=models.CASCADE,null=True, blank=True)
#     user = models.CharField(max_length=200,null=True)
#     name = models.CharField(max_length=200, null=True)
#     email = models.CharField(max_length=200,null=True)

#     def __str__(self):
#         return self.name

class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=50)
    brand = models.CharField(max_length=200, default="")
    price = models.IntegerField(default=0)
    composition = models.CharField(max_length=300)
    pub_date = models.DateField(default=timezone.now)
    expiry_date = models.DateField(default=timezone.now)
    quantity = models.PositiveBigIntegerField(default=1)
    image = models.ImageField(null=True,blank=TRUE, upload_to='medicines/images', default="")

    def __str__(self):
        return self.product_name
    
  
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url=''
        return url

class Order(models.Model):
    user = models.CharField(max_length=20,null=True, blank=False)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    payment_method = models.CharField(max_length=20, choices=METHOD, default="Cash On Delivery")
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS,default="Order Received")
    transaction_id = models.CharField(max_length=200, null=True)


    def __str__(self):
        return str(self.id)
    
    @property
    def shipping(self):
        shipping = False
        # orderitems = self.orderitem_set.all()
        # for i in orderitems:
        #     if i.product_name.digital == False:
        #         shipping = True
       
        return shipping
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

class OrderItem(models.Model):
    
    product_name = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0,null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    
    

    @property
    def get_total(self):
        total = self.product_name.price *self.quantity
        return total


class ShippingAddress(models.Model):
    City=(
    ('Kathmandu','Kathmandu'),
    ('Bhaktapur','Bhaktapur'),
    ('Lalitpur','Lalitpur'),)
    user = models.CharField(max_length=20,null=True, blank=False)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=100, null=True )
    city = models.CharField(max_length=100,choices=City, null=True )
    ward_no = models.IntegerField(null=True)
    zip_code = models.IntegerField(null=True)
    phone = models.IntegerField(blank=True,null=True)
    pres = models.ImageField(null=True,blank=True,upload_to='medicines/images/', default="")
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user
        
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url=''
        return url
        


class Wishlist(models.Model):
    user = models.CharField(max_length=20,null=True, blank=False)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)


# class Prescription(models.Model):
#     user = models.CharField(max_length=20,null=True, blank=False)
#     pres = models.ImageField(null=True,blank=False, upload_to='medicines/prescription', default="")


# class completedOrder(models.Model):
#     user = models.CharField(max_length=20,null=True, blank=False)
#     order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)

