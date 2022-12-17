from django.db import models
from django.utils.html import mark_safe
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
  name=models.CharField(max_length=100)
  description=models.TextField()
  photo = models.ImageField(upload_to="category_imgs/", null=True)
  itemNo=models.PositiveIntegerField(default=0)

  class Meta:
    verbose_name_plural='Categories'

  def photo_tag(self):
    return mark_safe('<img src="%s" width="40" height="40" />' % (self.photo.url))  

  def __str__(self):
    return self.name

class Item(models.Model):
  name=models.CharField(max_length=200)
  slug = models.CharField(max_length=400, null=True)
  description=models.TextField()
  category= models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
  price = models.PositiveIntegerField()
  photo = models.ImageField(upload_to="item_imgs/")
  inStock = models.PositiveIntegerField()
  status=models.BooleanField(default=True)

  class Meta:
    verbose_name_plural='Items'

  def photo_tag(self):
    return mark_safe('<img src="%s" width="40" height="40" />' % (self.photo.url))

  def __str__(self):
    return self.name

class Size(models.Model):
  title=models.CharField(max_length=100)

  class Meta:
    verbose_name_plural='Sizes'

  def __str__(self):
    return self.title

class ItemAttribute(models.Model):
  item=models.ForeignKey(Item, on_delete=models.CASCADE)
  size=models.ForeignKey(Size, on_delete=models.CASCADE)

  class Meta:
    verbose_name_plural='Item Attributes'

  def __str__(self):
    return self.item.name

status_choice=(
  ('Processing','Processing'),
  ('Shipping','Shipping'),
  ('Delivered','Delivered'),
)
class Order(models.Model):
  user=models.ForeignKey(User, on_delete=models.CASCADE)
  totalAmount=models.FloatField()
  orderStatus=models.CharField(max_length=100,choices=status_choice, default='Processing')
  orderDate=models.DateTimeField(auto_now_add=True)

  class Meta:
    verbose_name_plural='Orders'

class OrderItems(models.Model):
  order=models.ForeignKey(Order,on_delete=models.CASCADE)
  orderNumber=models.CharField(max_length=150)
  item=models.CharField(max_length=150)
  image=models.CharField(max_length=200)
  quantity=models.IntegerField()
  price=models.FloatField()
  total=models.FloatField()

  class Meta:
    verbose_name_plural='Order Items'

  def photo_tag(self):
    return mark_safe('<img src="/media/%s" width="40" height="40" />' % (self.image))

class UserData(models.Model):
  user=models.ForeignKey(User, on_delete=models.CASCADE)
  age=models.IntegerField()
  phoneno=models.CharField(max_length=15)
  address=models.CharField(max_length=1000)

  class Meta:
    verbose_name_plural='User Data'