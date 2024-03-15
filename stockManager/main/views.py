from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
import openfoodfacts

from stocks.models import Product, Stock

class ReadBarcodeForm(forms.Form):
    barcode = forms.CharField(label="Barcode");

def index(request):
    if request.method == "POST":
        form = ReadBarcodeForm(request.POST);

        if form.is_valid():
            barcode = form.cleaned_data["barcode"];
            
            try:
                product = Product.objects.get(serialNumber=barcode);
            except Product.DoesNotExist:
                api = openfoodfacts.API(user_agent="MyAwesomeApp/1.0");
                response = api.product.get(barcode, fields=["code", "product_name", "image_front_url"]);

                if response == None:
                    p = Product.objects.create(
                        serialNumber=barcode,
                        name='missing',
                        type="default",
                        image="https://salonlfc.com/wp-content/uploads/2018/01/image-not-found-scaled-1150x647.png",
                    );
                    p.save();
                    s = Stock.objects.create(product=p, quantity=1);
                    s.save();
                    return redirect(f"stocks/product/{p.id}");
                else:
                    p = Product.objects.create(
                        serialNumber=barcode,
                        name=response['product_name'],
                        type="default",
                        image=response['image_front_url'],
                    );
                    p.save();
                    s = Stock.objects.create(product=p, quantity=1);
                    s.save();      
                    return redirect(f"stocks/{s.id}");         
            try:
                stock = Stock.objects.get(product=product);
                stock.quantity = stock.quantity + 1;
                stock.save();
            
                return redirect(f"stocks/{stock.id}");
            except (Stock.DoesNotExist):
                return render(request, "main/index.html", {
                    "form": ReadBarcodeForm()
                });
        else:
            return render(request, "main/index.html", {
                "form": form
            });
    return render(request, "main/index.html", {
        "form": ReadBarcodeForm()
    });

def about(request):
    return render(request, "main/about.html");
