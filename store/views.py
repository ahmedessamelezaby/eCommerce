from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime
# from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def store(request):
  if request.user.is_authenticated:
    customer=request.user.customer
    order, created = Order.objects.get_or_create(customer=customer,completed=False)
    items=order.orderitem_set.all()
    cartItems = order.get_cart_items
  else:
    items = []
    order = {'get_cart_total':0,'get_cart_items':0,'shipping':False}
    cartItems = order['get_cart_items']
  
  products= Product.objects.all()
  
  return render(request,'store/store.html',{
    'products':products,
    'cartItems':cartItems,
    })

def cart(request):
  if request.user.is_authenticated:
    customer=request.user.customer
    order, created = Order.objects.get_or_create(customer=customer,completed=False)
    items=order.orderitem_set.all()
    cartItems = order.get_cart_items
  else:
    items = []
    order = {'get_cart_total':0,'get_cart_items':0,'shipping':False}
    cartItems = order['get_cart_items']
  
  return render(request,'store/cart.html',{
    'items':items,
    'order':order,
    'cartItems':cartItems
  })

# @csrf_exempt
def checkout(request):
  if request.user.is_authenticated:
    customer=request.user.customer
    order, created = Order.objects.get_or_create(customer=customer,completed=False)
    items=order.orderitem_set.all()
    cartItems = order.get_cart_items
  else:
    items = []
    order = {'get_cart_total':0,'get_cart_items':0,'shipping':False}
    cartItems = order['get_cart_items']
  return render(request,'store/checkout.html',{
    'items':items,
    'order':order,
    'cartItems':cartItems
  })


def updateItem(request):
  # body from cart.js
  data = json.loads(request.body)
  productId=data['productId']
  action = data['action']
  print(productId)
  print(action)
  
  customer = request.user.customer
  product = Product.objects.get(id=productId)
  order, created = Order.objects.get_or_create(customer=customer,completed = False)
  orderItem, created = OrderItem.objects.get_or_create(product=product,order=order)
  if action == 'add':
    orderItem.quantity = (orderItem.quantity + 1)
  elif action == 'remove':
    orderItem.quantity = (orderItem.quantity - 1)
  
  orderItem.save()
  
  if orderItem.quantity <= 0:
    orderItem.delete()
  return JsonResponse('Item was added',safe=False)

def processOrder(request):
  transaction_id = datetime.datetime.now().timestamp()
  data = json.loads(request.body)
  
  if request.user.is_authenticated:
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer,completed=False)
    total = float(data['form']['total'])
    order.transaction_id=transaction_id
    
    if total == order.get_cart_total:
      order.completed = True
    order.save()
    
    if order.shipping == True:
      ShippingAddress.objects.create(
        customer=customer,
        order=order,
        # shipping from js in checkout.html
        address=data['shipping']['address'],
        city=data['shipping']['city'],
        state=data['shipping']['state'],
        zipcode=data['shipping']['zipcode'],
        
      )
  else:
    print('User is not logged in..')
  return JsonResponse('Payment completed!',safe=False)