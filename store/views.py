from django.shortcuts import render
from .models import *
from django.http import JsonResponse
# Create your views here.

def store(request):
  products= Product.objects.all()
  return render(request,'store/store.html',{
    'products':products
    })

def cart(request):
  if request.user.is_authenticated:
    customer=request.user.customer
    order, created = Order.objects.get_or_create(customer=customer,completed=False)
    items=order.orderitem_set.all()
  else:
    items = []
    order = {'get_cart_total':0,'get_cart_items':0}
  
  return render(request,'store/cart.html',{
    'items':items,
    'order':order,
  })

def checkout(request):
  if request.user.is_authenticated:
    customer=request.user.customer
    order, created = Order.objects.get_or_create(customer=customer,completed=False)
    items=order.orderitem_set.all()
  else:
    items = []
    order = {'get_cart_total':0,'get_cart_items':0}
    
  return render(request,'store/checkout.html',{
    'items':items,
    'order':order,
  })


def updateItem(request):
  return JsonResponse('Item was added',safe=False)