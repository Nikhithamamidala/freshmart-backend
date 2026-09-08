from rest_framework import serializers
from ..models.order import Cart, CartItem, Order, OrderItem, Payment
from .catalog_serializers import ProductSerializer

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']
        depth = 1

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    class Meta:
        model = Cart
        fields = ['id', 'items']

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'user', 'full_name', 'mobile_number', 'shipping_address', 'payment_method', 'total_amount', 'discount_applied', 'final_amount', 'status', 'created_at', 'items']