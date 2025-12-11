from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product   # make sure Product model exists
from cart.models import Order
from django.contrib import messages


# ----------------------------
# ADMIN DASHBOARD
# ----------------------------
def admin_dashboard(request):
    products = Product.objects.all()

    if request.method == "POST":
        name = request.POST.get("name")
        price = request.POST.get("price")
        category = request.POST.get("category")
        description = request.POST.get("description")
        image = request.FILES.get("image")

        Product.objects.create(
            name=name,
            price=price,
            category=category,
            description=description,
            image=image
        )

        return redirect("admin_dashboard")

    return render(request, "adminpanel/dashboard.html", {"products": products})


# ----------------------------
# MANAGE PRODUCTS PAGE
# ----------------------------
def manage_products(request):
    products = Product.objects.all()
    return render(request, "adminpanel/manage_products.html", {"products": products})


# ----------------------------
# EDIT PRODUCT
# ----------------------------
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        product.name = request.POST.get("name")
        product.price = request.POST.get("price")
        product.category = request.POST.get("category")
        product.description = request.POST.get("description")

        if request.FILES.get("image"):
            product.image = request.FILES.get("image")

        product.save()
        return redirect("manage_products")

    return render(request, "adminpanel/edit_product.html", {"product": product})


# ----------------------------
# DELETE PRODUCT
# ----------------------------
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect("manage_products")




def admin_orders(request):
    orders = Order.objects.all().order_by('-id')  # newest first
    return render(request, 'adminpanel/orders.html', {'orders': orders})



def approve_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.status = "Processing"
    order.save()

    messages.success(request, f"Order #{order.id} approved successfully.")
    return redirect("admin_orders")   # ✔ correct URL name



def track_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "adminpanel/track_order.html", {"order": order})

def reject_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.status = "Rejected"
    order.save()

    messages.error(request, f"Order #{order.id} has been rejected.")
    return redirect("admin_orders")


def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        new_status = request.POST.get("status")
        order.status = new_status
        order.save()

        messages.success(request, f"Order #{order.id} updated to {new_status}.")
        return redirect("admin_orders")




