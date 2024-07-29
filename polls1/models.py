from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class Category(models.Model):
    DEVICE_CHOICES = [
        ("Mobile", "Mobile"),
        ("Tablet", "Tablet"),
        ("Laptop",'Laptop'),
        ("Watch","Watch"),
        ("Gadget","Gadget"),
        ("Speaker","Speaker"),
        ("Accessories","Accessories"),
        ("Computer","Computer"),
    ]
    name = models.CharField(max_length=100, choices=DEVICE_CHOICES)

    def __str__(self) -> str:
        return self.name


class Brand(models.Model):
    brand_name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.brand_name


class ProductModel(models.Model):

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="assets/img/")
    item_title = models.CharField(max_length=100)
    item_desc = models.CharField(max_length=200)
    price = models.IntegerField(default=0)
    item_discount_price = models.IntegerField(default=0)
    Trending_product = models.BooleanField(default=False,help_text="@-default,1-Trending")


class ProductDescription(models.Model):
    name = models.CharField(max_length=100)
    desc = models.CharField(max_length=300)
    image = models.ImageField(upload_to="assets/img/")


class Review(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    review = models.CharField(max_length=150)
    rating = models.IntegerField(default=0)

    def clean(self):
        if not (1 <= self.rating <= 5):
            raise ValidationError("Rating must be between 1 and 5")


class AddToCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    price = models.IntegerField(default=0)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self) -> str:
        return self.product.brand.brand_name
    
class OrderProductDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    price = models.IntegerField(default=0)
    quantity = models.PositiveIntegerField(default=1)
    name = models.CharField(max_length=100)



class ContactUs(models.Model):
    name = models.CharField(max_length=100)
    email =models.EmailField(default="123@gmail.com")
    subject = models.CharField(max_length=100)
    message =models.CharField(max_length=150)

    def __str__(self) -> str:
        return self.name
    
class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name =models.CharField(max_length=100)
    last_name =models.CharField(max_length=100)
    company_name =models.CharField(max_length=100, blank=True, null=True)
    area_code =models.CharField(max_length=100)
    primary_phone = models.CharField(max_length=100)
    street_address = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=100)
    business_address = models.BooleanField(default=False,blank=True,null=True)


    def __str__(self):
        return self.user.username

class Faq(models.Model):
    question =  models.CharField(max_length=100)
    answer = models.CharField(max_length=500)
class AboutUs(models.Model):
    heading = models.CharField(max_length=100)
    paragraph =models.CharField(max_length=100)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    forget_password_token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username