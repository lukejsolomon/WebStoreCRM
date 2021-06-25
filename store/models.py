from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200)

	def __str__(self):
		return self.name

class Tag(models.Model):
	name = models.CharField(max_length=200, null=True)

	def __str__(self):
		return self.name

class Product(models.Model):
	sCATEGORY = (
			('Summer', 'Summer'),
			('Winter', 'Winter'),
			)
	gCATEGORY = (
			('Womens', 'Womens'),
			('Mens', 'Mens'),
			) 
	LOCATION = (
			('001','001'),
			('002','002'),
			('003','003'),
			('004','004'),
			('005','005'),
			('006','006'),
			('007','007'),

			) 
	name = models.CharField(max_length=200)
	description = models.CharField(max_length=200, null=True, blank=True)
	genderCategory = models.CharField(max_length=200, null=True, choices=gCATEGORY)
	seasonCategory = models.CharField(max_length=200, null=True, choices=sCATEGORY)

	price = models.FloatField()
	slPrice = models.FloatField(null=True, blank=True)
	lwstPrice = models.FloatField(null=True, blank=True)

	cost = models.FloatField(null=True, blank=True)
	location = models.CharField(max_length=200, null=True, choices=LOCATION)
	mnfDscptn = models.TextField(null=True, blank=True)
	mnfBrCd = models.CharField(max_length=200, default=False)
	digital = models.BooleanField(default=False,null=True, blank=True)
	
	image = models.ImageField(null=True, blank=True)
	image2 = models.ImageField(null=True, blank=True)
	image3 = models.ImageField(null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	tags = models.ManyToManyField(Tag)

	newItem = models.BooleanField(default=False,null=True, blank=True)
	whatsHot = models.BooleanField(default=False,null=True, blank=True)
	promo = models.BooleanField(default=False,null=True, blank=True)

	def __str__(self):
		return self.name

	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url

class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)
	transaction_id = models.CharField(max_length=100, null=True)

	def __str__(self):
		return str(self.transaction_id)
		
	@property
	def shipping(self):
		shipping = False
		orderitems = self.orderitem_set.all()
		for i in orderitems:
			if i.product.digital == False:
				shipping = True
		return shipping

	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total 

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total 

class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	

	@property
	def get_total(self):
		total = self.product.price * self.quantity
		return total

class ShippingAddress(models.Model):
	STATUS = (
			('Pending', 'Pending'),
			('Picked', 'Picked'),
			('Shipped', 'Shipped'),
			('Canceled', 'Canceled'),
			)
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	##addition
	#use foreignkey to save an item per delivery
	# orderItem = models.ForeignKey(OrderItem, on_delete=models.SET_NULL, null=True)
	#use manytomany to save multiple items per delivery
	orderItem = models.ManyToManyField(OrderItem)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	state = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=200, null=True,blank=True, choices=STATUS, default="Pending")
	note = models.CharField(max_length=1000, null=True, blank=True)

	def __str__(self):
		return self.address


