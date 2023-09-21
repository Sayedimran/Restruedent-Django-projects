from django.shortcuts import render,redirect
from django.views import View
from . models import Product,Customer,Cart, OrderPlaced
from . forms import customarResgistrationFrom
from  django.contrib import messages
# Create your views here.
class ProductView(View):
    def get(self, request):
        Books = Product.objects.filter(category = 'B')
        Electronics = Product.objects.filter(category = 'E')
        foods= Product.objects.filter(category = 'F')
        cooking = Product.objects.filter(category = 'CO')
        organicfood = Product.objects.filter(category = 'Org')
        
        
        return render(request, 'Shop/home.html', {'Books':Books, 'Electronics':Electronics, 'foods': foods , 'cooking': cooking , 'organicfood':organicfood , })



class ProductDetailView(View):
  def get(self,request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, 'Shop/productdetail.html',{'product': product})

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
      
   



# def add_to_cart(request):
#  return render(request, 'Shop/addtocart.html')

# def buy_now(request):
#  return render(request, 'Shop/buynow.html')

# def profile(request):
#  return render(request, 'Shop/profile.html')

# def address(request):
#  return render(request, 'Shop/address.html')

# def orders(request):
#  return render(request, 'Shop/orders.html')

# def change_password(request):
#  return render(request, 'Shop/changepassword.html')


# def login(request):
#      return render(request, 'Shop/login.html')

# def customerregistration(request):
#  return render(request, 'Shop/customerregistration.html')

# def checkout(request):
#  return render(request, 'Shop/checkout.html')
