from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Customer(models.Model):
  user=models.OneToOneField(User,null=True,blank=True, on_delete=models.CASCADE)
  name=models.CharField(max_length=100,null=True)
  email=models.EmailField(max_length=200)
  
  def __str__(self) -> str:
    return self.name

class Product(models.Model):
  name=models.CharField(max_length=100,null=True)
  price=models.DecimalField(max_digits=7,decimal_places=2)
  digital=models.BooleanField(default=False,null=True,blank=True)
  image =models.ImageField(upload_to='image',null=True,blank=True)
  def __str__(self) -> str:
    return self.name
  
  @property
  def imageURL(self):
    try:
      url=self.image.url
    except:
      url = ''
    return url

class Order(models.Model):
  customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True)
  date_ordered=models.DateTimeField(auto_now_add=True)
  completed=models.BooleanField(default=False)
  transaction_id=models.CharField(max_length=100,null=True)
  
  def __str__(self) -> str:
    return str(self.id)
  
  @property
  def shipping(self):
    shipping = False
    order_item=self.orderitem_set.all()
    for i in order_item:
      if i.product.digital == False:
        shipping = True
    return shipping
  
  @property
  def get_cart_total(self):
    order_item=self.orderitem_set.all()
    total = sum([item.get_total for item in order_item])
    return total
  
  @property
  def get_cart_items(self):
    order_item=self.orderitem_set.all()
    total = sum([item.quantity for item in order_item ])
    return total

class OrderItem(models.Model):
  product=models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
  order=models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)
  quantity=models.IntegerField(default=0,null=True,blank=True)
  date_added=models.DateTimeField(auto_now_add=True)
  
  def __str__(self) -> str:
    return self.product.name
  
  @property
  def get_total(self):
    total = self.product.price * self.quantity
    return total
  
  
class ShippingAddress(models.Model):
  customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True)
  order=models.ForeignKey(Order,on_delete=models.SET_NULL,null=True,blank=True)
  address=models.CharField(max_length=100,null=True)
  city=models.CharField(max_length=100,null=True)
  state=models.CharField(max_length=100,null=True)
  zipcode=models.CharField(max_length=100,null=True)
  date_added=models.DateTimeField(auto_now_add=True)
  
  def __str__(self) -> str:
    return self.address