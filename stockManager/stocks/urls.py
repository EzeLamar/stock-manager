from django.urls import path
from . import views

app_name = "stocks";
urlpatterns = [
    path("", views.index, name="stocks"),
    path("<int:id_stock>", views.stock, name="stock"),
    path("product/<int:id_product>", views.editProduct, name="product"),
];
