from rest_framework import serializers
from ..models.catalog import Product, Category

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'unit', 'stock', 'image_url', 'category']  # <--- Added 'unit'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'