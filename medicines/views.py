from audioop import reverse
from email import message
from itertools import product
from multiprocessing import context
from django.shortcuts import render
from matplotlib.pyplot import get
from matplotlib.style import available
from numpy import save
from sklearn.preprocessing import OrdinalEncoder
from .models import *
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import json
from plyer import notification
import datetime

# Create your views here.


# home page
def index_page(request):
    if request.user.is_authenticated:
        title = " WELCOME TO AAUSADHI PASAL "
        message = "Thank you for choosing us!!!"
        notification.notify(title= title,
                    message= message,
                    app_icon = None,
                    timeout= 5,
                    toast=False)
        order, created = Order.objects.get_or_create(user=request.user.username,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = [] 
        order = {'get_cart_total':0,'get_cart_items':0}
        cartItems= order['get_cart_items']
    context = {'cartItems': cartItems}
    return render(request, 'index.html',context)

def store(request):
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(user= request.user.username,complete=False)
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
        order, created = Order.objects.get_or_create(user=request.user.username,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        # order = {'get_cart_total':0, 'get_cart_items':0}
    
    context = {'items': items, 'order':order,'cartItems': cartItems}
    return render(request, 'cart.html',context)

def checkout(request):

    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(user=request.user.username,complete=False)
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
        order, created = Order.objects.get_or_create(user=request.user.username,complete=False)
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

    
    product_name = Product.objects.get( id=productId)
    order, created = Order.objects.get_or_create(user=request.user.username,complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product_name=product_name)

    if action =='add':
        orderItem.quantity = (orderItem.quantity + 1)

    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity -1)
    orderItem.save()

    if orderItem.quantity <=0:
        orderItem.delete()

    return JsonResponse('Item was added',safe=False)


def remove_from_cart(request, id):
    if request.method == 'POST':
        delb = OrderItem.objects.get(product_name_id=id)
        delb.delete()
        return HttpResponseRedirect('/cart')
 
def ProcessOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(user=request.user.username,complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        if order.shipping == False:
             ShippingAddress.objects.create(
                user = request.user.username,
                order = order,
                address = data['shipping']['address'],
                city = data['shipping']['city'],
                ward_no = data['shipping']['ward_no'],
                zip_code = data['shipping']['zip_code'],

            )


    return JsonResponse('payment submited',safe=False)