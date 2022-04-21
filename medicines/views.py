from audioop import reverse
from email import message
from itertools import product
from multiprocessing import context
from django.shortcuts import redirect, render
from matplotlib.pyplot import get
from matplotlib.style import available
from numpy import save
import requests
from sklearn.preprocessing import OrdinalEncoder
from .models import *
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import json
from plyer import notification
import datetime
from django.views.decorators.csrf import csrf_exempt


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

def remove_from_wishlist(request, id):
    if request.method == 'POST':
        delb = Wishlist.objects.get(user = request.user.username, product_id=id)
        delb.delete()
        return HttpResponseRedirect('/wishlist')
 
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
                pres = data['shipping']['pres'],
                phone = data['shipping']['phone'],

            )


    return JsonResponse('payment submited',safe=False)



@csrf_exempt
def khalti(request):
   data = request.POST
   product_id = data['product_identity']
   token = data['token']
   amount = data['amount']

   url = "https://khalti.com/api/v2/payment/verify/"
   payload = {
   "token": token,
   "amount": amount
   }
   headers = {
   "Authorization": "test_public_key_dc74e0fd57cb46cd93832aee0a390234"
   }
   
   response = requests.post(url, payload, headers = headers)
   
   response_data = json.loads(response.text)
   status_code = str(response.status_code)

   if status_code == '400':
      response = JsonResponse({'status':'false','message':response_data['detail']}, status=500)
      return response

   import pprint 
   pp = pprint.PrettyPrinter(indent=4)
   pp.pprint(response_data)
   
   return JsonResponse(f"Payment Success !! . {response_data['user']['idx']}",safe=False)

@login_required(login_url='login')
def searchBar(request):
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(user=request.user.username,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        if request.method == 'GET':
            query = request.GET.get('query')
        if query:
            products = Product.objects.filter(product_name__icontains=query) 
            return render(request, 'searchbar.html', {'products':products,'items': items, 'order':order, 'cartItems':cartItems})
        else:
            items = []
            print("No information to show")
        return render(request, 'searchbar.html', {})


def wishlist(request):
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(user=request.user.username,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items    
        wishlist= Wishlist.objects.filter(user=request.user)

    return render(request,'wishlist.html',{'wishlist':wishlist,'items': items, 'order':order, 'cartItems':cartItems})

def addtowishlist(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            
            product_check = Product.objects.get(id=prod_id)
            if(product_check):
                if(Wishlist.objects.filter(user=request.user, product_id= prod_id)):
                    return JsonResponse({'status':"Product already in wishlist"})
                else:
                    Wishlist.objects.create(user=request.user,product_id = prod_id)
                    return JsonResponse({'status':"product added to wishlist"})

            else:
                return JsonResponse({'status':"No such product found"})

        
        else:
            return JsonResponse({'status':"login to contibue"})
    return redirect('/')

# def deletewishlistitem(request):
#     if request.method == "POST":
#         if request.user.is_authenticated:
#             prod_id = int(request.POST.get('product_id'))
#             if(Wishlist.objects.filter(user=request.user, product_id= prod_id)):
#                 wishlistitem = Wishlist.objects.get(product_id = prod_id)
#                 wishlistitem.delete()
#                 return JsonResponse({'status':"Product removed from wishlist"})
#             else:
#                 return JsonResponse({'status':"Product not found in wishlist"})

        
#         else:
#             return JsonResponse({'status':"login to contibue"})
#     return redirect('/')