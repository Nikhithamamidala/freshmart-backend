from django.db import transaction  # <--- ADD THIS LINE HERE
from django.contrib.auth.models import User
from ..models import Order, OrderItem, Payment
from .cart_service import get_cart_for_user

@transaction.atomic
def checkout(user: User, data: dict):
    cart = get_cart_for_user(user)
    if not cart.items.exists():
        raise ValueError("Cart is empty")
    # ... rest of your code ...