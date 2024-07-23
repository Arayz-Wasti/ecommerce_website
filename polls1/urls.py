from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('index_fixed_header/',views.index_fixed_header, name='index_fixed_header'),
    path('index_inverse_header/',views.index_inverse_header, name='index_inverse_header'),
    # path("product_view/<slug:pk>",views.product_list_view,name="product_view"),
    # path('<str:brand_name>/', views.filter_by_brand, name='filter_by_brand'),
    path('delete/<int:id>',views.DeleteProduct,name='DeleteProduct'),
    path("about_us/", views.about, name="about_us"),
    path("product/", views.product, name="product"),
    path("product_detail/<int:pk>", views.product_detail, name="product_detail"),
    path("checkout_cart/", views.checkout_cart, name="checkout_cart"),
    path("increment/<int:id>/", views.increment_quan, name="increment_quan"),
    path("decrement/<int:id>/", views.decrement_quan, name="decrement_quan"),
    path("checkout_complete/", views.checkout_complete, name="checkout_complete"),
    path("checkout_info/", views.checkout_info, name="checkout_info"),
    path("checkout_payment/", views.checkout_payment, name="checkout_payment"),
    path("my_account/", views.my_account, name="my_account"),
    path("contact_us/", views.contact_us, name="contact_us"),
    path("faq/", views.faq, name="faq"),
    path("search_results/", views.search_results, name="search_results"),
    path('sign/',views.user_signUp,name='user_signIn'),
    path('log_in/', views.user_log_in, name='log_in'),
    path('log_out/', views.log_out, name='log_out'),
    path('product-category/<str:product_category>/',views.product,name='product_category')
]
