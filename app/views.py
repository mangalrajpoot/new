from django.shortcuts import render,redirect
from app.models import Product
from django.views import View
from .models import Product,Customer,Cart,OrderPlaced
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.db.models import Q 
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator




def home(request):
 totalitem=0
 if request.user.is_authenticated:
  totalitem=len(Cart.objects.filter(user=request.user))

  mobile=Product.objects.filter(category='M')
  laptop=Product.objects.filter(category='L')
  topwear=Product.objects.filter(category='TW')
  bottom=Product.objects.filter(category='BW')
  return render(request, 'app/home.html',{'d':mobile,'laptop':laptop,'topwear':topwear,'bottom':bottom,'totalitem':totalitem})

class ProductView(View):
 def get(self,request):
  totalitem=0
  if request.user.is_authenticated:
    totalitem=len(Cart.objects.filter(user=request.user))
    topwears=Product.objects.filter(category='TW')
    bottomwears=Product.objects.filter(categary='BW')
    mobiles=Product.objects.filter(category='M')
    laptops=Product.objects.filter(category='L')
  
  
    return render(request,'app/home.html',{'topwears':topwears,'bottomwears':bottomwears,'mobiles':mobiles,'laptops':laptops,'totalitem':totalitem})
  




# def product_detail(request):
#  return render(request, 'app/productdetail.html')


@method_decorator(login_required,name='dispatch')
class ProductDetailView(View):
 def get(self,request,pk):
  product=Product.objects.get(pk=pk)
  already_item=False
  totalitem=0
  if request.user.is_authenticated:
    already_item=Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
    totalitem=len(Cart.objects.filter(user=request.user))
  return render(request, 'app/productdetail.html',{'product':product,'already_item':already_item,'totalitem':totalitem})

@login_required
def add_to_cart(request): 
  user=request.user
  product_id=request.GET.get('prod-id')
  product=Product.objects.get(id=product_id)
  
  if user.is_authenticated:
    
    Cart(user=user,product=product).save()
    return redirect('/cart')
  else:
   return redirect('login')
 

@login_required
def show_cart(request):
 totalitem=0
 if request.user.is_authenticated:
  totalitem=len(Cart.objects.filter(user=request.user))
  user=request.user
  cart=Cart.objects.filter(user=user)
  amount=0.0
  shipping_amount=70.0
  total_amount=0.0
  cart_product=[p for p in Cart.objects.all() if p.user==user]
  if cart_product:
   for p in cart_product:
    tempamount=(p.quantity*p.product.discounted_price)
    amount=amount+tempamount
    total_amount=amount+shipping_amount

    return render(request, 'app/addtocart.html',{'carts':cart,'total_amount':total_amount,'amount':amount,'totalitem':totalitem})
  else:
   return render(request, 'app/emptycart.html')
 return render(request, 'app/emptycart.html')

@login_required
def buy_now(request):
 return render(request, 'app/buynow.html')


@login_required
def address(request):
 totalitem=0
 if request.user.is_authenticated:
  totalitem=len(Cart.objects.filter(user=request.user))

  add=Customer.objects.filter(user=request.user)
  return render(request, 'app/address.html',{'address':add,'active':'btn-primary','totalitem':totalitem})


@login_required
def orders(request):
 op=OrderPlaced.objects.filter(user=request.user)
 return render(request, 'app/orders.html',{'orderplaced':op})


def mobile(request,data=None):
  if data==None:
    mobiles=Product.objects.filter(category='M')
  elif data=='Redmi' or data=='Samsung' or data=='Real':
    mobiles=Product.objects.filter(category='M').filter(brand=data)
  elif data=='below':
    mobiles=Product.objects.filter(category='M').filter(discounted_price__lt=10000)
  elif data=='above':
    mobiles=Product.objects.filter(category='M').filter(discounted_price__gt=10000)
  return render(request, 'app/mobile.html',{'mobiles':mobiles})

# def login(request):
#   return render(request, 'app/login.html')

# def customerregistration(request):
#return render(request, 'app/customerregistration.html')

def laptop(request,ldata=None):
  if ldata==None:
    laptops=Product.objects.filter(category='L')
  elif ldata=='LG' or ldata=='Lenovo' or ldata=='Asus' or ldata=='Samsung':
    laptops=Product.objects.filter(category='L').filter(brand=ldata)
  elif ldata=='below':
    laptops=Product.objects.filter(category='L').filter(discounted_price__lt=10000)
  elif ldata=='above':
    laptops=Product.objects.filter(category='L').filter(discounted_price__gt=10000)
  return render(request,'app/laptop.html',{'laptops':laptops})


# def topwear(request,twdata=None):
#   if twdata==None:
#     topwear=Product.objects.filter(category='TW')
#   elif twdata=='John' or twdata=='Sharda' or twdata=='Vinayak' or twdata=='Siyaram':
#     topwear=Product.objects.filter(category='TW').filter(brand=twdata)
#   elif twdata=='below':
#     topwear=Product.objects.filter(category='TW').filter(discounted_price__lt=10000)
#   elif twdata=='above':
#     topwear=Product.objects.filter(category='TW').filter(discounted_price__gt=10000)
#   return render(request,'app/topwear.html',{'topwear':topwear})


def topwear(request,twdata=None):
  if twdata==None:
    topwear=Product.objects.filter(category='TW')
  elif twdata=='John' or twdata=='Sharda' or twdata=='Vinayak' or twdata=='Siyaram':
    topwear=Product.objects.filter(category='TW').filter(brand=twdata)
  elif twdata=='below':
    topwear=Product.objects.filter(category='TW').filter(discounted_price__lt=1000)
  elif twdata=='above':
    topwear=Product.objects.filter(category='TW').filter(discounted_price__gt=1000)
  return render(request,'app/topwear.html',{'topwear':topwear})

def bottomwear(request,bwdata=None):
  if bwdata==None:
    bottomwear=Product.objects.filter(category='BW')
  elif bwdata=='Lee' or bwdata=='Ben' or bwdata=='Pepe' or bwdata=='Neo':
    bottomwear=Product.objects.filter(category='BW').filter(brand=bwdata)
  elif bwdata=='below':
    bottomwear=Product.objects.filter(category='BW').filter(discounted_price__lt=1000)
  elif bwdata=='above':
    bottomwear=Product.objects.filter(category='BW').filter(discounted_price__gt=1000)
  return render(request,'app/bottomwear.html',{'bottomwear':bottomwear})





class CustomerRegistrationView(View):
  def get(self,request):
   form=CustomerRegistrationForm()
  
   return render(request, 'app/customerregistration.html',{'form':form})
  def post(self,request):
    form=CustomerRegistrationForm(request.POST)
    if form.is_valid():
      messages.success(request,'Congratulation!! Registeration Success !')
      form.save()
    return render(request, 'app/customerregistration.html',{'form':form})

   
@login_required
def checkout(request):
 user=request.user
 add=Customer.objects.filter(user=user)
 cart_items=Cart.objects.filter(user=user)
 amount=0.0
 shipping_amount=70.0
 totalamount=0.0
 cart_product=[p for p in Cart.objects.all() if p.user==request.user]
 if cart_product:
  for p in cart_product:
   tempamount=(p.quantity*p.product.discounted_price)
   amount=amount+tempamount
  totalamount=amount+shipping_amount

 return render(request, 'app/checkout.html',{'add':add,'totalamount':totalamount,'cartitems':cart_items})

@login_required
def payment_done(request):
 user=request.user
 custid=request.GET.get('custid')
 customer=Customer.objects.get(id=custid)
 cart=Cart.objects.filter(user=user)
 for c in cart:
  OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
  c.delete()
 return redirect('orders')
 

@method_decorator(login_required,name='dispatch')
class ProfileView(View):
 def get(self,request):
  totalitem=0
  if request.user.is_authenticated:
    totalitem=len(Cart.objects.filter(user=request.user))
    form=CustomerProfileForm()
    return render(request,'app/profile.html',{'form':form,'active':'btn-primary','totalitem':totalitem})
 def post(self,request):
  form=CustomerProfileForm(request.POST)
  if form.is_valid():
   usr=request.user
   name=form.cleaned_data['name']
   locality=form.cleaned_data['locality']
   city=form.cleaned_data['city']
   state=form.cleaned_data['state']
   zipcode=form.cleaned_data['zipcode']
   reg=Customer(user=usr,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
   reg.save()
   messages.success(request,'Congratulation!! Profile Updated Successfully')
  return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})


def plus_cart(request):
 if request.method=='GET':
  prod_id=request.GET['prod_id']
  c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
  c.quantity=c.quantity+1
  c.save()
  amount=0.0
  shipping_amount=70.0
  cart_product=[p for p in Cart.objects.all() if p.user==request.user]
  for p in cart_product:
   tempamount=(p.quantity*p.product.discounted_price)
   amount=amount+tempamount
   total_amount=amount+shipping_amount
  data={
    'quantity':c.quantity,
    'amount':amount,
    'totalamount':total_amount
   }
  return JsonResponse(data)



def minus_cart(request):
 if request.method=='GET':
  prod_id=request.GET['prod_id']
  c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
  c.quantity=c.quantity-1
  c.save()
  amount=0.0
  shipping_amount=70.0
  cart_product=[p for p in Cart.objects.all() if p.user==request.user]
  for p in cart_product:
   tempamount=(p.quantity*p.product.discounted_price)
   amount=amount+tempamount
   total_amount=amount+shipping_amount
  data={
    'quantity':c.quantity,
    'amount':amount,
    'totalamount':total_amount
   }
  return JsonResponse(data)

def remove_cart(request):
 if request.method=='GET':
  prod_id=request.GET['prod_id']
  c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
  
  c.delete()
  amount=0.0
  shipping_amount=70.0
  cart_product=[p for p in Cart.objects.all() if p.user==request.user]
  for p in cart_product:
   tempamount=(p.quantity*p.product.discounted_price)
   amount=amount+tempamount
   
  data={
    
    'amount':amount,
    'totalamount':amount+shipping_amount,
   }
  return JsonResponse(data)
 else:
  return HttpResponse("")
 
   
  
  




















