from django.shortcuts import render
from adminpanel.models import Product  # Product model from adminpanel

def product_list(request):
    products = Product.objects.all()
    return render(request, "products/product_list.html", {"products": products})