import stripe
from django.urls import reverse
# from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import datetime
from django.http import HttpResponse
from polls1.models import *
from .utils import send_email_to_user,forget_password_email
from ecom_web import settings
stripe.api_key = settings.STRIPE_SECRET_KEY
import uuid

def user_signUp(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return HttpResponse('Passwords do not match')

        if User.objects.filter(username=username).exists():
            return HttpResponse('Username already exists')

        user = User.objects.create_user(username=username, email=email, password=password)
        profile_user = Profile.objects.create(user = user)
        profile_user.save()
        user.save()

        return redirect('log_in')
    else:
        return render(request, 'signIn.html')

def user_log_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  
        else:
            return HttpResponse('Invalid username or password')
    else:
        return render(request, 'LogIn.html')
    
def log_out(request):
    logout(request)
    return redirect('log_in')

def password_reset(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('Username') 
            user_flex = User.objects.get(username=username)
            token=str(uuid.uuid4())
            profile_obj = Profile.objects.get(user=user_flex)
            profile_obj.forget_password_token = token
            profile_obj.save()
            forget_password_email(profile_obj.user.email,token)
            return redirect('log_in')
    except Exception as e:
        print(e)
    return render(request,'password_reset.html')

def forget_password(request,token):
    context = {}
    try:
        profile_user = Profile.objects.filter(forget_password_token=token).first()
        if request.method == 'POST':
            new_pass = request.POST.get('New Password')
            con_pass = request.POST.get('Confirm Password')
            if new_pass!=con_pass:
                return HttpResponse("password are invalid!")
            user_id = request.POST.get('userId')
            user_obj = User.objects.get(id= user_id)
            user_obj.set_password(new_pass)
            user_obj.save()
            return redirect('log_in')
        context = {
            'user_id':profile_user.user.id,
        }
        
    except Exception as e:
        print(e)
    return render(request,'forget_password.html',context)
    
    
@login_required
def home(request):

    mobile =request.GET.get('mobile')
    print(mobile)

    if mobile:

        mobile_products = ProductModel.objects.filter(category__name="Mobile" , brand__brand_name=mobile)[:6]
    else:
        mobile_products = ProductModel.objects.filter(category__name="Mobile")


    # tablet_products = ProductModel.objects.filter(category__name="Tablet")[:6]

    user = request.user


    trending_product  = ProductModel.objects.filter(Trending_product=1)[:6]

    brand_name = Brand.objects.all()
    

    category = Category.objects.all()

    
    selected_brand = request.GET.get('tablet', None)
    
    if selected_brand:
        products = ProductModel.objects.filter  (brand__brand_name=selected_brand, category__name="Tablet")
    else:
        products = ProductModel.objects.filter  (category__name="Tablet")


    tablet_products = products[:6]
 
    

    # category_products = ProductModel.objects.all()
        
    product_apple=ProductModel.objects.filter(brand__brand_name="Apple")
    product_sumsung=ProductModel.objects.filter(brand__brand_name="Sumsung")
    product_sony=ProductModel.objects.filter(brand__brand_name="Sony")
    product_microsoft=ProductModel.objects.filter(brand__brand_name="Microsoft")

    product_item_title = ProductModel.objects.get(item_title="iPhone SE")
    product_watch = ProductModel.objects.get(item_title="Apple Watch")
    product_mac = ProductModel.objects.get(item_title="Mac Mini")
    product_mac_pro = ProductModel.objects.get(item_title="Mac Pro")
    product_accessories = ProductModel.objects.get(item_title="Apple Accessories")
    product_laptop = ProductModel.objects.get(item_title="Macbook Air")
    product_6s = ProductModel.objects.get(item_title="iPhone 6s")
    product_comp = ProductModel.objects.get(item_title="iMac")
    product_edge= ProductModel.objects.get(item_title="Galaxy s7 Edge")
    cart_items = AddToCart.objects.all()

    
    data = {
        'user':user,
        "mobile_products": mobile_products,
        "tablet_products": tablet_products,
        'Trending_product':trending_product,
        'category':category,
        'product_apple':product_apple,
        'product_sumsung':product_sumsung,
        'product_sony':product_sony,
        'product_microsoft':product_microsoft,
        'product_item_title':product_item_title,
        'product_watch':product_watch,
        'product_mac':product_mac,
        'product_mac_pro':product_mac_pro,
        'product_accessories':product_accessories,
        'product_laptop':product_laptop,
        'product_6s':product_6s,
        'product_comp':product_comp,
        'product_edge':product_edge,
        'brand_names': brand_name,
        # 'category_products': category_products,
        'products': products,
        'cart_items':cart_items,
    }
    
    return render(request, "index.html",data)

def index_fixed_header(request):
    return render(request,'index_fixed_header.html')
def index_inverse_header(request):
    return render(request,'index_inverse_header.html')


def header(request):
    cart_items = AddToCart.objects.all()
    data={
        "cart_items":cart_items,
    }
    return render(request,'header.html',data)

def about(request):

    abt_us_mod = AboutUs.objects.all()
    data ={'abt_us_mod':abt_us_mod}

    return render(request, "about_us.html",data)


def product(request):
    mobile_products = ProductModel.objects.filter(category__name="Mobile")
    tablet_products = ProductModel.objects.filter(category__name="Tablet")
    items = ProductModel.objects.all()
    categories = Category.objects.all()
    
    paginator = Paginator(items, 6)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'items': page_obj,
        'categories': categories,
        'prod': categories,
        'mobile_products':mobile_products,
        'tablet_products':tablet_products,
    }
    
    return render(request, "product.html",context=context)


@login_required
def product_detail(request, pk):
    # products = product_mod.objects.filter(category__id=pk, )
    # print(products)
    product = get_object_or_404(ProductModel, pk=pk)
    product_desc = ProductDescription.objects.all()
    reviews = Review.objects.filter(product=product)

    if request.method == "POST":
        name = request.POST.get("name")
        title = request.POST.get("Title")
        review = request.POST.get("review")
        rating = int(request.POST.get("rating"))
        print(review)
        try:
            product = ProductModel.objects.get(id=2)
        except ProductModel.DoesNotExist:
            print("Product with id 2 does not exist.")
        else:
   
            review = Review(product=product, rating=5)
            review.save()

        try:
            new_review = Review(
                product=product, name=name, title=title, review=review, rating=rating
            )
            new_review.full_clean()
            new_review.save()
        except ValidationError as e:
            context = {
                "product": product,
                "product_desc": product_desc,
                "reviews": reviews,
            }

        return redirect("product_detail", pk=pk)

    context = {
        "product": product,
        "product_desc": product_desc,
        "reviews": reviews,
    }
    return render(request, "product_detail.html", context=context)

@login_required
def checkout_cart(request):

    if request.method == "POST":
        productid = request.POST.get("prod_id")
        products = get_object_or_404(ProductModel, id=productid)
        AddToCart.objects.create(
            user=request.user,product=products, image=products.image, price=products.price,
        )
        return redirect('checkout_cart')
        
    amount = 0
    shipping = 0 
    total_amount = 0
    cart_items = AddToCart.objects.all()

    if cart_items:
        for cart in cart_items:
            cart.total_price = cart.price * cart.quantity
            total_price  = cart.price * cart.quantity
            shipping +=cart.quantity * 8
            amount += total_price
            total_amount += shipping + total_price

  
      # cart_totals = sum(item.price * item.quantity for item in cart_items)

    # cart_total = sum(item.price * item.quantity for item in cart_items)rint(cart_total)
    context={"cart_items": cart_items, 
             "amount":amount,
             "shipping":shipping,
             "subtotal":total_amount,
             
             
             }
    return render(
        request,
        "checkout_cart.html",
        context=context,
    )

def increment_quan(request,id):
    cart_item  = get_object_or_404(AddToCart,id=id)
    cart_item.quantity+=1
    cart_item.save()
    return redirect('checkout_cart')

def decrement_quan(request,id):
    cart_item  = get_object_or_404(AddToCart,id=id)
    if cart_item.quantity > 1:
        cart_item.quantity-=1
        cart_item.save()
    return redirect('checkout_cart')

def DeleteProduct(request,id):
    product_id = get_object_or_404(AddToCart,id=id)
    product_id.delete()
    return redirect('checkout_cart')



@login_required
def checkout_info(request):
       
    error = []
    context = {'error': error}
    
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        company_name = request.POST.get('company_name')
        area_code = request.POST.get('area_code')
        primary_phone = request.POST.get('primary_phone')
        address_1 = request.POST.get('address_1')
        address_2 = request.POST.get('address_2')
        street_address = f"{address_1} {address_2}".strip()
        zip_code = request.POST.get('zip_code')
        business_address = request.POST.get('business_address')

        
        if not first_name:
            error.append("Invalid user name")
        if not last_name:
            error.append("Invalid last name")
        if not area_code or len(area_code) > 3:
            error.append("Invalid area code")
        if not primary_phone:
            error.append("Invalid primary phone")
        if not street_address:
            error.append("Invalid street address")
        if not zip_code:
            error.append("Invalid zip code")

        if not error:
            shipping_address = ShippingAddress(
                user=request.user,
                first_name=first_name,
                last_name=last_name,
                company_name=company_name,
                area_code=area_code,
                primary_phone=primary_phone,
                street_address=street_address,
                zip_code=zip_code,
                business_address=business_address
            )
            shipping_address.save()
            return redirect('checkout_payment')
    return render(request, "checkout_info.html",context)


@login_required
def checkout_payment(request):
    user_cart_items = AddToCart.objects.filter(user=request.user)
    if user_cart_items.exists():
        line_items = []
        for cart_item in user_cart_items:
            product = cart_item.product
            name = product.item_title
            price = product.price
            line_items.append({
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': int(price * 100),
                        'product_data': {'name': name},
                    },
                    'quantity': cart_item.quantity,
                })
            session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            mode='payment',
            success_url=request.build_absolute_uri(reverse('checkout_complete')),
            cancel_url=request.build_absolute_uri(reverse('home')),
            line_items=line_items,
            )
                # return HttpResponse('Success')
            send_email_to_user()
            return redirect(session.url)
    return render(request, "checkout_payment.html")

# def send_email(request):
#     send_email_to_user()
#     return redirect('/')

def checkout_complete(request):
    items = AddToCart.objects.filter(user=request.user).first()
    cart_items = AddToCart.objects.filter(user=request.user)
    for i in cart_items:
        price=i.price
        image=i.image
        name = i.product.item_title
        quantity = i.quantity

        odr_prd_mod = OrderProductDetails.objects.create(user=request.user,name=name,image=image,price=price,quantity=quantity)
        odr_prd_mod.save()
   
    date = datetime.datetime.now()
    delivery_date_delta = datetime.timedelta(days=2)
    delivery_date = date + delivery_date_delta
    
    transaction = "REF" 
    bank_authorised_code = "AUTH" 

    cart_items_list = list(cart_items)

    cart_items.delete()

    context = {
        'items': items,
        'cart_items': cart_items_list, 
        'date': date,
        'delivery_date': delivery_date,
        'transaction_reference_no': transaction,
        'bank_authorised_code': bank_authorised_code,
    }
    return render(request, "checkout_complete.html", context)

def my_account(request):
    return render(request, "my_account.html")


def contact_us(request):

    try:
        if request.method == 'POST':
            name = request.POST.get("name")
            email = request.POST.get("email")
            subject = request.POST.get("subject")
            message = request.POST.get("message")

            ContactModel =ContactUs.objects.create(name=name,email=email,subject=subject,message=message)
            ContactModel.save()


            return redirect("contact_us")
        
        else:
            return render(request, "contact_us.html")

    except Exception as e:
        print(f"Something went wrong${e}")



def faq(request):
    faq = Faq.objects.all()
    
    data = {
        'faq':faq,
    }
    return render(request, "faq.html",data )


def search_results(request):
    
    return render(request, "search_results.html")


# def product_list_view(request, pk):
#     products = ProductModel.objects.filter(category__id=pk)
#     paginator = Paginator(products, 3)  # Show 10 products per page

#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     context = {
#         'products': page_obj,
#     }
#     return render(request, 'product.html', context=context)
# def product(request, product_category=None):
#     items = ProductModel.objects.all()
#     categories = Category.objects.all()
    
#     if product_category:
#         items = ProductModel.objects.filter(product_category__category_name=product_category)
#     paginator = Paginator(items, 6)  
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
    
#     context = {
#         'items': page_obj,
#         'categories': categories,
#         'prod': product_category
#     }
#     return render(request, 'product.html', context)