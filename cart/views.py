from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from adminpanel.models import Product
from .models import CartItem

#
from django.urls import reverse
from django.contrib import messages
from .models import Order, OrderItem, CartItem
from adminpanel.models import Product
from decimal import Decimal

@login_required
def cart_page(request):
    items = CartItem.objects.filter(user=request.user)
    
    # calculate subtotal for each item
    for item in items:
        item.subtotal = item.product.price * item.quantity

    # calculate grand total
    grand_total = sum(item.subtotal for item in items)

    return render(request, "cart/cart_page.html", {"items": items, "grand_total": grand_total})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        item.quantity += 1
    
    item.save()
    return redirect("cart_page")


@login_required
def update_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)

    action = request.POST.get("action")

    if action == "increase":
        item.quantity += 1
    elif action == "decrease" and item.quantity > 1:
        item.quantity -= 1

    item.save()
    return redirect("cart_page")


@login_required
def remove_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()
    return redirect("cart_page")




#

@login_required
def checkout_page(request):
    # load cart items
    cart_items = CartItem.objects.filter(user=request.user).select_related("product")
    if not cart_items.exists():
        messages.warning(request, "Your cart is empty.")
        return redirect("products:list")  # adjust to your products list url

    # compute totals
    grand_total = sum(Decimal(item.product.price) * item.quantity for item in cart_items)

    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()
        phone = request.POST.get("phone", "").strip()
        address = request.POST.get("address", "").strip()
        city = request.POST.get("city", "").strip()
        postal_code = request.POST.get("postal_code", "").strip()
        country = request.POST.get("country", "").strip()
        payment_method = request.POST.get("payment_method", "cod")  # cod / test

        if not (full_name and phone and address):
            messages.error(request, "Please fill in name, phone and address.")
            return render(request, "cart/checkout.html", {"items": cart_items, "grand_total": grand_total})

        # create order
        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            phone=phone,
            address=address,
            city=city,
            postal_code=postal_code,
            country=country,
            total_amount=grand_total,
            payment_method=payment_method,
            payment_status="unpaid" if payment_method != "gateway" else "paid",  # adapt for real gateway
        )

        # create order items
        for ci in cart_items:
            OrderItem.objects.create(
                order=order,
                product=ci.product,
                quantity=ci.quantity,
                price=ci.product.price,
            )

        # empty cart
        cart_items.delete()

        # If using an external payment gateway, redirect to payment flow here.
        messages.success(request, f"Order placed successfully (Order #{order.id}).")
        return redirect("order_detail", order_id=order.id)

    return render(request, "cart/checkout.html", {"items": cart_items, "grand_total": grand_total})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "cart/order_history.html", {"orders": orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "cart/order_detail.html", {"order": order})

