from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from stocks.models import Stock, Product

class StockForm(forms.Form):
    quantity = forms.IntegerField(label="Units");

class ProductForm(forms.Form):
    name = forms.CharField(label="Name");
    serialNumber = forms.CharField(label="Barcode");
    type = forms.CharField(label="Type");
    image = forms.URLField(label="Image");

def index(request):
    stocks = Stock.objects.all();
    return render(request, "stocks/index.html", {
        "stocks": stocks,
    });

def stock(request, id_stock):
    try:
        stock = Stock.objects.get(id=id_stock);
    except Stock.DoesNotExist:
        return HttpResponseRedirect(reverse("stocks:stocks"));
    
    if request.method == "POST":
        form = StockForm(request.POST);
    
        if form.is_valid():
           quantity =  form.cleaned_data["quantity"];
   
        stock.quantity = quantity;
        stock.save();
        
        return HttpResponseRedirect(reverse("stocks:stocks"));

    form = StockForm();
    form["quantity"].initial = stock.quantity;
    return render(request, "stocks/stock.html", {
        "stock": stock,
        "form": form,
    })

def editProduct(request, id_product):
    try:
        product = Product.objects.get(id=id_product);
        stock = Stock.objects.get(product=product);
    except Product.DoesNotExist or Stock.DoesNotExist:
        return HttpResponseRedirect(reverse("stocks:stocks"));

    if request.method == "POST":
        form = ProductForm(request.POST);
    
        if form.is_valid():
           name =  form.cleaned_data["name"];
           barcode =  form.cleaned_data["serialNumber"];
           type =  form.cleaned_data["type"];
           image = form.cleaned_data["image"];

           product.name = name;
           product.serialNumber = barcode;
           product.type = type;
           product.image = image;
           product.save();
            
           return HttpResponseRedirect(reverse("stocks:stock", kwargs={'id_stock': stock.id}));
    
    form = ProductForm();
    form["name"].initial = product.name;
    form["type"].initial = product.type;
    form["image"].initial = product.image;
    form["serialNumber"].initial = product.serialNumber;
    
    return render(request, "products/set.html", {
        "form": form,
        "product": product,
        "stock": stock,
    })