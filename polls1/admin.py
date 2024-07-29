from django.contrib import admin
from polls1.models import *


# Register your models here.
@admin.register(Category)
class category_mod_reg(admin.ModelAdmin):
    list_display = ["id" ,"name"]


@admin.register(Brand)
class brand_mod_reg(admin.ModelAdmin):
    list_display = ["id" ,"brand_name", "category"]


@admin.register(ProductModel)
class product_mod_reg(admin.ModelAdmin):
    list_display = [
        "id",
        "brand",
        "category",
        "image",
        "item_title",
        "item_desc",
        "price",
        "item_discount_price",
        "Trending_product",
    ]


@admin.register(ProductDescription)
class ProductDescModl(admin.ModelAdmin):
    list_display = ["name", "desc", "image"]


@admin.register(Review)
class ReviewModelAdmin(admin.ModelAdmin):
    list_display = ["name", "title", "review", "rating"]


@admin.register(AddToCart)
class AddToCartAdmin(admin.ModelAdmin):
    list_display = ["user","product", "image", "price", "quantity"]

@admin.register(OrderProductDetails)
class OrderDetail(admin.ModelAdmin):
    list_display=['user','name','image','price','quantity']

@admin.register(ContactUs)
class ContactUsReg(admin.ModelAdmin):
    list_display=['name','email','subject','message']

@admin.register(ShippingAddress)
class ShippingAddressMod(admin.ModelAdmin):
    list_display = ['user','first_name','last_name','company_name','area_code','primary_phone','street_address','zip_code','business_address']
@admin.register(Faq)
class FaqModelReg(admin.ModelAdmin):
    list_display = ['question','answer']
@admin.register(AboutUs)
class AboutUs(admin.ModelAdmin):
    list_display = ['heading','paragraph']
@admin.register(Profile)
class AboutUs(admin.ModelAdmin):
    list_display = ['user','forget_password_token','created_at']