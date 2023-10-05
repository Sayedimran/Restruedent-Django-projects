from django.shortcuts import render,redirect
from django.views import View
from . models import Product,Customer,Cart, OrderPlaced
from . forms import customarResgistrationFrom
from  django.contrib import messages
from . forms import CustomerProfileForm
from . models import Customer
from django .db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import  method_decorator
# Create your views here.
class ProductView(View):
    def get(self, request):
        totalitem = 0

        Books = Product.objects.filter(category = 'B')
        Electronics = Product.objects.filter(category = 'E')
        foods= Product.objects.filter(category = 'F')
        cooking = Product.objects.filter(category = 'CO')
        organicfood = Product.objects.filter(category = 'Org')
        if request.user.is_authenticated:
           totalitem = len(Cart.objects.filter(user=request.user ))
        
        return render(request, 'Shop/home.html', {'Books':Books, 'Electronics':Electronics, 'foods': foods , 'cooking': cooking , 'organicfood':organicfood , 'totalitem':totalitem})


class ProductDetailView(View):
  def get(self,request, pk):
    totalitem = 0
    product = Product.objects.get(pk=pk)
    item_already_in_cart = False
    if request.user.is_authenticated:
       item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
       totalitem = len(Cart.objects.filter(user=request.user ))
      
           
   
    return render(request, 'Shop/productdetail.html',{'product': product, 'item_already_in_cart':item_already_in_cart, 'totalitem':totalitem })


# class ProductDetailView(View):
#   def get(self,request, pk):
#     product = Product.objects.get(pk=pk)
#     item_alrady_in_cart = False
#     if request.user.is_authenticated:
#        item_alrady_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists
       
#     return render(request, 'Shop/productdetail.html',{'product': product,'item_already_in_cart':item_alrady_in_cart})
    




def Electronicss( request, data =None ):
   if data == None:
      Electronic = Product.objects.filter(category = 'E')
   elif data == 'Watch' or data == 'infinity':
      Electronic = Product.objects.filter(category ='E').filter( brand = data)
   elif data == 'below':
      Electronic = Product.objects.filter(category = 'E').filter(discounted_price__lt =10000)
   elif data == 'above':
      Electronic = Product.objects.filter(category = 'E').filter(discounted_price__gt =10000)
   return render (request,'Shop/Electronics.html' ,{'Electronic':Electronic})

def login(request):
   return render(request,'Shop/login.html')

class customerRegistrationview(View):
   def get(self,request):
      form = customarResgistrationFrom()
      return render(request,'Shop/cutomerRegistraton.html',{'form':form})

   def post(self,request):
      form = customarResgistrationFrom(request.POST)
      if form.is_valid():
         messages.success(request,'Congratulations  registrations done')
      
         form.save()
      return render(request,'Shop/cutomerRegistraton.html',{'form':form})
      
   




@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
      form = CustomerProfileForm
      return render(request, 'Shop/profile.html', {'form':form, 'active':'btn-primary'})
   
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            division = form.cleaned_data['division']
            district = form.cleaned_data['district']
            thana = form.cleaned_data['thana']
            villorroad = form.cleaned_data['villorroad']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr,name=name, division=division,district=district, thana=thana, villorroad=villorroad, zipcode=zipcode)
            reg.save()
            messages.success(request, 'Congratulations! Profile Updated Successfully')
        return render(request, 'Shop/profile.html', {'form':form, 'active':'btn-primary'})




def address(request):
 add = Customer.objects.filter(user=request.user)
 return render(request, 'Shop/address.html',{'add':add, 'active':'btn-primary'})


def change_password(request):
 return render(request, 'Shop/changepassword.html' )

@login_required
def add_to_cart(request):
 user = request.user
 Product_id = request.GET.get('product_id')
 product = Product.objects.get(id=Product_id)      
 Cart(user=user,product=product,).save()
 return redirect('/cart')


@login_required
def show_cart(request):
  if request.user.is_authenticated:
      user = request.user
      cart = Cart.objects.filter(user=user)
      amount = 0.0
      shiping_amount = 100.0
      total = 0.0
      cart_product  = [p for p in Cart.objects.all() if p.user==user ]
      if cart_product:
         for p in cart_product:
            tempamount = (p.quantity*p.product.selling_price)
            amount += tempamount
            totalamount  = amount + shiping_amount
         return render(request,'Shop/addTocart.html',{'carts':cart ,'totalamount':totalamount,'amount':amount})
      else:
          return render(request,'Shop/emtycart.html')


def plus_cart(request):
   if request.method == "GET":
      product_id = request.GET['product_id']
      C = Cart.objects.get(Q(product=product_id) & Q(user=request.user))

      C.quantity += 1
      C.save()
      amount = 0.0
      shiping_amount = 100.0
      cart_product  = [d for d in Cart.objects.all() if d.user==request.user ]
      
      for d in cart_product:
            tempamount = (d.quantity*d.product.selling_price)
            amount += tempamount
            totalamount  = amount + shiping_amount
      data = {
        'quantity':C.quantity,
        'amount': amount,
        'totalamount':totalamount,

        }
      return JsonResponse(data)



def minus_cart(request):
   if request.method == "GET":
      product_id = request.GET['product_id']
      f = Cart.objects.get(Q(product=product_id) & Q(user=request.user))

      f.quantity -= 1
      f.save()
      amount = 0.0
      shiping_amount = 100.0
      cart_product  = [f for f in Cart.objects.all() if f.user==request.user ]
      
      for f in cart_product:
            tempamount = (f.quantity*f.product.selling_price)
            amount += tempamount
            totalamount  = amount + shiping_amount
      data = {
        'quantity':f.quantity,
        'amount': amount,
        'totalamount':totalamount,

        }
      return JsonResponse(data)


#Remove cart
def remove_cart(request):
    if request.method == 'GET':
      product_id = request.GET['product_id']
      c = Cart.objects.get(Q(product=product_id) & Q(user=request.user))
      c.delete()
      amount = 0
      shipping_amount = 100
      cart_product = [p for p in Cart.objects.all() if p.user==request.user]
      for p in cart_product:
            tempamount = (p.quantity * p.product.selling_price)
            amount += tempamount  
            totalamount = amount + shipping_amount
      data = {
         'amount': amount,
         'totalamount': totalamount
      }
      return JsonResponse(data)

@login_required 
def checkout(request):
 user = request.user
 add = Customer.objects.filter(user=user)
 cart_items = Cart.objects.filter(user=user)
 amount = 0.0
 shipping_amount = 100.0
 totalamount = 0.0
 cart_product = [p for p in Cart.objects.all() if p.user==user]
 if cart_product:
         for p in cart_product:
            tempamount = (p.quantity * p.product.selling_price)
            amount += tempamount  
         totalamount = amount + shipping_amount 
 return render(request, 'Shop/checkout.html',{'add':add, 'totalamount':totalamount, 'cart_items':cart_items })



def orders(request):
 op = OrderPlaced.objects.filter(user=request.user)
 return render(request, 'Shop/orders.html', {'order_placed':op})



def payment_done(request):
   user = request.user
   custid = request.GET.get('custid')
   customer = Customer.objects.get(id=custid)
   cart = Cart.objects.filter(user=user)
   for c in cart:
      OrderPlaced(user=user, customer=customer, product = c.product, quantity = c.quantity).save()
      c.delete()

   return redirect('orders') 


