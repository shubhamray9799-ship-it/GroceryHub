from django.urls import path
from . import views
from .views import approve_order, track_order

urlpatterns = [
    path("", views.admin_dashboard, name="admin_dashboard"),

    path("manage-products/", views.manage_products, name="manage_products"),

    path("edit-product/<int:product_id>/", views.edit_product, name="edit_product"),

    path("delete-product/<int:product_id>/", views.delete_product, name="delete_product"),

    path("admin_orders/", views.admin_orders, name="admin_orders"),

    path("order/<int:order_id>/approve/", approve_order, name="approve_order"),

    path("order/<int:order_id>/track/", track_order, name="track_order"),

    path("order/<int:order_id>/reject/", views.reject_order, name="reject_order"),

    path("order/<int:order_id>/update-status/", views.update_order_status, name="update_order_status"),





]


