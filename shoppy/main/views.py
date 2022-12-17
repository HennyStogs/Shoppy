from django.shortcuts import render, redirect
from .models import Category, Item, ItemAttribute, Order, OrderItems, UserData
from django.http import JsonResponse,HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.db.models import Min,Max
from .forms import RegistrationForm
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.conf import settings
from paypal.standard.forms import PayPalPaymentsForm

# Create your views here.
def homepage(request):
  data=Item.objects.all().order_by('-id')[:4]
  return render(request, 'index.html', {'data':data})

def categories(request):
  data=Category.objects.all().order_by('name')
  return render(request, 'categories.html', {'data':data})

def browse(request):
  data=Item.objects.all().order_by('name')
  categories=Item.objects.distinct().values('category__name','category__id')
  sizes=ItemAttribute.objects.distinct().values('size__title', 'size__id')
  priceminmax=Item.objects.aggregate(Min('price'),Max('price'))
  return render (request, 'browse.html', {'data':data, 'categories':categories, 'sizes':sizes, 'priceminmax':priceminmax})

def categoryitems (request, category_id):
  category=Category.objects.get(id=category_id)
  data = Item.objects.filter(category=category).order_by('-name')
  categories=Item.objects.distinct().values('category__name','category__id')
  sizes=ItemAttribute.objects.distinct().values('size__title', 'size__id')
  priceminmax=Item.objects.aggregate(Min('price'),Max('price'))
  return render(request, 'categoryitems.html', {'data':data, 'categories':categories, 'sizes':sizes, 'priceminmax':priceminmax})

def itempage (request, slug, id):
  item = Item.objects.get(id=id)
  return render(request, 'itempage.html', {'data': item})

def search(request):
  query=request.GET['q']
  data=Item.objects.filter(name__icontains=query).order_by('-id')
  return render(request, 'search.html', {'data':data})

def filter_data(request):
  categories=request.GET.getlist('category[]')
  sizes=request.GET.getlist('size[]')
  minPrice=request.GET['minPrice']
  maxPrice=request.GET['maxPrice']
  allItems=Item.objects.all().order_by('-id').distinct()
  allItems=allItems.filter(price__gte=minPrice)
  allItems=allItems.filter(price__lte=maxPrice)
  if len(categories)>0:
	  allItems=allItems.filter(category__id__in=categories).distinct()
  if len(sizes)>0:
    allItems=allItems.filter(itemattribute__size__id__in=sizes).distinct()
  finaldata=render_to_string('ajax/itemlist.html',{'data':allItems})
  return JsonResponse({'data':finaldata})

def addtocart(request):
  cartproducts={}
  cartproducts[str(request.GET['id'])]={
    'name':request.GET['name'], 'quantity':request.GET['quantity'], 'price':request.GET['price'], 'image':request.GET['image'],
  }
  if 'cartdata' in request.session:
    if str(request.GET['id']) in request.session['cartdata']:
      cart_data=request.session['cartdata']
      cart_data[str(request.GET['id'])]['quantity']=int(cartproducts[str(request.GET['id'])]['quantity'])
      cart_data.update(cart_data)
      request.session['cartdata']=cart_data
    else:
      cart_data=request.session['cartdata']
      cart_data.update(cartproducts)
      request.session['cartdata']=cart_data
  else:
    request.session['cartdata']=cartproducts
  return JsonResponse({'data':request.session['cartdata'], 'totalitems':len(request.session['cartdata'])})

def deletefromcart(request):
  itemid=request.GET['id']
  if 'cartdata' in request.session:
    if itemid in request.session['cartdata']:
      cart_data=request.session['cartdata']
      del request.session['cartdata'][itemid]
      request.session['cartdata']=cart_data
  totalprice=0
  for itemid,item in request.session['cartdata'].items():
    totalprice=totalprice+(int(item['quantity'])*float(item['price']))
  finaldata=render_to_string('ajax/cartlist.html',{'cartdata':request.session['cartdata'], 'totalitems':len(request.session['cartdata']), 'totalprice':totalprice})
  return JsonResponse({'data':finaldata, 'totalitems':len(request.session['cartdata'])})

def updatecart(request):
  itemid=request.GET['id']
  itemquantity=request.GET['quantity']
  if 'cartdata' in request.session:
    if itemid in request.session['cartdata']:
      cart_data=request.session['cartdata']
      cart_data[str(request.GET['id'])]['quantity']=itemquantity
      request.session['cartdata']=cart_data
  totalprice=0
  for itemid,item in request.session['cartdata'].items():
    totalprice=totalprice+(int(item['quantity'])*float(item['price']))
  finaldata=render_to_string('ajax/cartlist.html',{'cartdata':request.session['cartdata'], 'totalitems':len(request.session['cartdata']), 'totalprice':totalprice})
  return JsonResponse({'data':finaldata, 'totalitems':len(request.session['cartdata'])})

def cart(request):
  totalprice=0
  if 'cartdata' in request.session:
    for itemid,item in request.session['cartdata'].items():
      totalprice=totalprice+(int(item['quantity'])*float(item['price']))
    return render(request, 'cart.html', {'cartdata':request.session['cartdata'], 'totalitems':len(request.session['cartdata']), 'totalprice':totalprice})
  else:
    return render(request, 'cart.html', {'cartdata':'','totalitems':0,'totalprice':totalprice})

@login_required
def checkout(request):
  totalprice=0
  total_price=0
  if 'cartdata' in request.session:
    for itemid,item in request.session['cartdata'].items():
      total_price=total_price+(int(item['quantity'])*float(item['price']))
    order=Order.objects.create(
      user=request.user,
      totalAmount=total_price
    )
    for itemid,item in request.session['cartdata'].items():
      totalprice=totalprice+(int(item['quantity'])*float(item['price']))
      items=OrderItems.objects.create(
        order=order,
        orderNumber=str(order.id),
        item=item['name'],
        image=item['image'],
        quantity=item['quantity'],
        price=item['price'],
        total=float(item['quantity'])*float(item['price'])
      )
    host = request.get_host()
    paypal_dict = {
      'business': settings.PAYPAL_RECEIVER_EMAIL,
      'amount': totalprice,
      'item_name': 'Order No:'+str(order.id),
      'invoice': 'INV-'+str(order.id),
      'currency_code': 'USD',
      'notify_url': 'http://{}{}'.format(host,reverse('paypal-ipn')),
      'return_url': 'http://{}{}'.format(host,reverse('paymentsuccessful')),
      'cancel_return': 'http://{}{}'.format(host,reverse('paymentcancelled')),
    }
    form = PayPalPaymentsForm(initial=paypal_dict)
    user=request.user
    userdata=UserData.objects.get(user=request.user)
    return render(request, 'checkout.html', {'cartdata':request.session['cartdata'], 'totalitems':len(request.session['cartdata']), 'totalprice':totalprice, 'form':form, 'user':user, 'userdata':userdata})

@csrf_exempt
def paymentsuccessful(request):
	returnData=request.POST
	return render(request, 'paymentsuccessful.html',{'data':returnData})


@csrf_exempt
def paymentcancelled(request):
	return render(request, 'paymentcancelled.html')

def ordersuccessful(request):
  # send_mail('Order Confirmed',
  # 'This is an email that confirms that your order has been placed!',
  # 'shoppy327@gmail.com',
  # ['hoteki9382@lubde.com'],
  # fail_silently=False)
  return render(request, 'ordersuccessful.html')

def register(request):
  if request.method=='POST':
    form=RegistrationForm(request.POST)
    if form.is_valid():
      form.save()
      username=form.cleaned_data.get('username')
      password=form.cleaned_data.get('password1')
      age=form.cleaned_data.get('age')
      address=form.cleaned_data.get('address')
      phoneno=form.cleaned_data.get('phoneno')
      user=authenticate(username=username, password=password)
      login(request,user)
      userdata=UserData.objects.create(
        user=user,
        age=age,
        phoneno=phoneno,
        address=address
      )
      return redirect('registersuccessful')
  form=RegistrationForm
  return render(request, 'registration/register.html', {'form':form})

def registersuccessful(request):
  return render(request, 'registersuccessful.html')

def account(request):
  return render(request, 'account.html')

def orders(request):
  orders=Order.objects.filter(user=request.user).order_by('-id')
  return render(request, 'orders.html', {'orders':orders})

def orderitems(request,id):
  order=Order.objects.get(pk=id)
  orderitems=OrderItems.objects.filter(order=order).order_by('-id')
  return render(request, 'orderitems.html', {'orderitems':orderitems})

def userdetails(request):
  user=request.user
  userdata=UserData.objects.get(user=request.user)
  return render(request, 'userdetails.html',{'user':user, 'userdata':userdata})