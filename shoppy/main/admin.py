from django.contrib import admin
from .models import Category, Item, Size, ItemAttribute, Order, OrderItems, UserData
# Register your models here.


admin.site.register(Size)

class CategoryAdmin(admin.ModelAdmin):
  list_display=('id', 'name', 'photo_tag')
admin.site.register(Category, CategoryAdmin)

class ItemAdmin(admin.ModelAdmin):
  list_display=('id','name','category','price','inStock','status', 'photo_tag')
  list_editable=('status',)
admin.site.register(Item, ItemAdmin)

class ItemAttributeAdmin(admin.ModelAdmin):
  list_display=('item','size')
admin.site.register(ItemAttribute, ItemAttributeAdmin)

class OrderAdmin(admin.ModelAdmin):
  list_display=('user','totalAmount','orderStatus','orderDate')
  list_editable=('orderStatus',)
admin.site.register(Order, OrderAdmin)

class OrderItemsAdmin(admin.ModelAdmin):
  list_display=('orderNumber','item','photo_tag','quantity','price','total')
admin.site.register(OrderItems, OrderItemsAdmin)

class UserDataAdmin(admin.ModelAdmin):
  list_display=('user','age','phoneno','address')
admin.site.register(UserData, UserDataAdmin)