from itertools import product
from multiprocessing import context
from django.shortcuts import render
from numpy import save
from sklearn.preprocessing import OrdinalEncoder
from .models import *
from django.http import JsonResponse
import json


# Create your views here.


# home page
def index_page(request):
    # if request.user.is_authenticated:
    #     customer = request.user.customer
    #     order, created = Order.objects.get_or_create(customer=customer,complete=False)
    #     items = order.orderitem_set.all()
    #     cartItems = order.get_cart_items
    # # else:
    #     items = [] 
    #     order = {'get_cart_total':0,'get_cart_items':0}
    #     cartItems= order['get_cart_items']
    return render(request, 'index.html')

def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []   
        # cartItems= order['get_cart_items']

    products = Product.objects.all()
    context = {'products':products,  'cartItems': cartItems}
    return render(request,'store.html',context)
 

def cart(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        # order = {'get_cart_total':0, 'get_cart_items':0}
    
    context = {'items': items, 'order':order,'cartItems': cartItems}
    return render(request, 'cart.html',context)

def checkout(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
    
    context = {'items': items, 'order':order, 'cartItems':cartItems}

    return render(request, 'checkout.html',context)

def prod_detail(request):
    return render(request, 'productdetails.html',context)


def prod_detail(request,id):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = [] 
    

    product = Product.objects.get(id=id)
    return render(request,'productdetails.html',{'cartItems':cartItems,'data':product})

from django.contrib.auth.decorators import login_required

@login_required
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:',action)
    print('Product:',productId)

    customer = request.user.customer
    product_name = Product.objects.get( id=productId)
    order, created = Order.objects.get_or_create(customer=customer,complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product_name=product_name)

    if action =='add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity -1)
    orderItem.save()

    if orderItem.quantity <=0:
        orderItem.delete()

    return JsonResponse('Item was added',safe=False)

