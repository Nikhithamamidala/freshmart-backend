from ..models import Category, Product
from django.shortcuts import get_object_or_404

# --- MANAGE CATEGORIES ---
def admin_get_categories():
    return Category.objects.all()

def admin_create_category(data):
    return Category.objects.create(**data)

def admin_update_category(category_id, data):
    category = get_object_or_404(Category, id=category_id)
    for key, value in data.items():
        setattr(category, key, value)
    category.save()
    return category

def admin_delete_category(category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    return True

# --- MANAGE VEGETABLES (Products) ---
def admin_get_products():
    return Product.objects.all()

def admin_create_product(data):
    return Product.objects.create(**data)

def admin_update_product(product_id, data):
    product = get_object_or_404(Product, id=product_id)
    for key, value in data.items():
        setattr(product, key, value)
    product.save()
    return product

def admin_delete_product(product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return True