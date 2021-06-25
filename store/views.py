from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponseRedirect
import json
import datetime
from .models import * 
from .utils import cookieCart, cartData, guestOrder
from store.forms import ShippingForm, ServiceForm

def store(request):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)

def productDetail(request, pk):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	products = Product.objects.get(id=pk)
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/productDetail.html', context)

def womens(request):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	products = Product.objects.filter(genderCategory='Womens')
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)

def mens(request):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	products = Product.objects.filter(genderCategory='Mens')
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)

def summer(request):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	products = Product.objects.filter(seasonCategory='Summer')
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)

def winter(request):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	products = Product.objects.filter(seasonCategory='Winter')
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)


def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)

def checkout(request):
	data = cartData(request)
	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()
	allorderitems = order.orderitem_set.all()##addition

	if order.shipping == True:
		##addition
		#use for foreignkey with orderitem
		# ShippingAddress.objects.create(
		# customer=customer,
		# order=order,
		# orderItem=allorderitems[0],
		# address=data['shipping']['address'],
		# city=data['shipping']['city'],
		# state=data['shipping']['state'],
		# zipcode=data['shipping']['zipcode'],
		# )
		#use for manytomanyfield with orderitem
		new_shipping = ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)
		for item in allorderitems:
			new_shipping.orderItem.add(item)
		new_shipping.save()

	return JsonResponse('Payment submitted..', safe=False)



	

def orders(request):
    order = Order.objects.all()
    item = OrderItem.objects.all()
    address = ShippingAddress.objects.all()
    context = {'order':order, 'address': address, 'item':item}
    return render(request, 'store/orders.html', context)


def shipping(request):
    order = Order.objects.all()
    item = OrderItem.objects.all()
    address = ShippingAddress.objects.filter(status='Pending')
    context = {'order':order, 'address': address, 'item':item}
    return render(request, 'store/shipping.html', context)


def pickTicket(request):
    order = Order.objects.all()
    item = OrderItem.objects.order_by('location')
    address = ShippingAddress.objects.filter(status='Pending')
    context = {'order':order, 'address': address, 'item':item}
    return render(request, 'store/pickTicket.html', context)

def updateOrder(request, pk):
    address = ShippingAddress.objects.get(id=pk)
    form = ShippingForm(request.POST or None, instance=address)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    context = {'address': address, 'form':form}
    return render(request, 'store/updateOrder.html', context)

def serviceOrder(request, pk):
    address = ShippingAddress.objects.get(id=pk)
    form = ServiceForm(request.POST or None, instance=address)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    context = {'address': address, 'form':form}
    return render(request, 'store/serviceOrder.html', context)


def service(request):
    order = Order.objects.all()
    item = OrderItem.objects.all()
    address = ShippingAddress.objects.all()
    context = {'order':order, 'address': address, 'item':item}
    return render(request, 'store/service.html', context)