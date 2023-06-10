from django.contrib import admin
from .models import *
from django.utils.html import format_html
from django.urls import reverse


@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display=('id','user','name','locality','city','zipcode','state')

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display=('id','title','selling_price','discounted_price','description','brand','category')

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display=('id','user','product','quantity')

@admin.register(OrderPlaced)
class OrderPlaced(admin.ModelAdmin):
    list_display=('id','user','customer','customer_info','product_info','product','quantity','ordered_date','status')
    def customer_info(self,obj):
        link=reverse("admin:app_customer_change",args=[obj.customer.pk])
        return format_html('<a href="{}">{}</a>',link,obj.customer.name)
    
    def product_info(self,obj):
        link=reverse("admin:app_product_change",args=[obj.customer.pk])
        return format_html('<a href="{}">{}</a>',link,obj.product.title)