from django.db import models

class Category(models.Model):
    category_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    status = models.CharField(max_length=20, default='active')

    def __str__(self):
        return self.category_name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    product_name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=20, default='kg')
    stock_quantity = models.IntegerField(default=0)
    image_url = models.URLField(blank=True, null=True)
    status = models.CharField(max_length=20, default='active')

    def __str__(self):
        return self.product_name

class Inventory(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='inventory')
    opening_stock = models.IntegerField(default=0)
    purchased = models.IntegerField(default=0)
    sold_stock = models.IntegerField(default=0)
    remaining = models.IntegerField(default=0)
    low_stock_limit = models.IntegerField(default=5)

class Offer(models.Model):
    offer_code = models.CharField(max_length=50)
    offer_type = models.CharField(max_length=20)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    minimum_order = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    status = models.CharField(max_length=20, default='active')

    def __str__(self):
        return self.offer_code