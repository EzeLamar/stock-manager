from django.db import models

class Product(models.Model):
    serialNumber = models.CharField(max_length=12);
    name = models.CharField(max_length=64);
    type = models.CharField(max_length=64);
    image = models.URLField();

    def __str__(self) -> str:
        return f"'{self.name}' ({self.type})";

##class Type(models.model):
### this table should include the type of products and the description to include in the Product

class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="products");
    quantity = models.PositiveIntegerField();

    def __str__(self) -> str:
        return f"{self.product} | {self.quantity}";
