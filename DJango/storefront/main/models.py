from django.db import models

# Create your models here.

class Category(models.Model):
    category = models.CharField(max_length=200)

    def __str__(self):
        return self.category  # This returns the category name

class Item(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null = True, blank=True)
    sku = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    quantity = models.IntegerField()
    supplier = models.CharField(max_length=200)

    def __str__(self):
        return self.sku

class Inbound(models.Model):
    product_sku = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, blank=True)
    reference = models.CharField(max_length=200)
    quantity = models.IntegerField()
    location = models.CharField(max_length=200)
    remarks = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        sku = self.product_sku.sku if self.product_sku else 'N/A'
        return f"{sku} - {self.date} - {self.location}"

class Outbound(models.Model):
    product_sku = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, blank=True)
    reference = models.CharField(max_length=200)
    quantity = models.IntegerField()
    destination = models.CharField(max_length=200)
    remarks = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product_sku.sku} - {self.date} - {self.destination}"
