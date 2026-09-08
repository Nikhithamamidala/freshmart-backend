from ..models import Cart, CartItem, Product
from django.shortcuts import get_object_or_404

def get_cart_for_user(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart

def add_to_cart(user, product_id, quantity):
    cart = get_cart_for_user(user)
    product = get_object_or_404(Product, id=product_id)
    
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not created: 
        item.quantity += quantity
    else: 
        item.quantity = quantity
        
    # CRITICAL: Update the 'price' field based on current quantity (matches ER diagram)
    item.price = product.price * item.quantity
    item.save()
    
    return cart

def update_cart_item(user, item_id, quantity):
    item = get_object_or_404(CartItem, id=item_id, cart__user=user)
    item.quantity = quantity
    
    # CRITICAL: Update the 'price' field based on current quantity
    item.price = item.product.price * item.quantity
    item.save()
    
    return item.cart

def remove_cart_item(user, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=user)
    item.delete()
    return item.cart