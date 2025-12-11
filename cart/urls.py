# from django.urls import path
# from . import views

# urlpatterns = [
#     path("", views.cart_page, name="cart_page"),
#     path("add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
#     path("update/<int:item_id>/", views.update_quantity, name="update_quantity"),
#     path("remove/<int:item_id>/", views.remove_item, name="remove_item"),
# ]



#
from django.urls import path
from . import views

urlpatterns = [
    path("", views.cart_page, name="cart_page"),
    path("add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("update/<int:item_id>/", views.update_quantity, name="update_quantity"),
    path("remove/<int:item_id>/", views.remove_item, name="remove_item"),

    # orders & checkout
    path("checkout/", views.checkout_page, name="checkout_page"),
    path("orders/", views.order_history, name="order_history"),
    path("orders/<int:order_id>/", views.order_detail, name="order_detail"),
]

