from .catalog_serializers import ProductSerializer, CategorySerializer
from .auth_serializers import RegisterSerializer, UserSerializer
from .order_serializers import CartSerializer, CartItemSerializer, OrderSerializer, OrderItemSerializer
from .admin_serializers import AdminOrderStatusUpdateSerializer, AdminUserUpdateSerializer
from rest_framework import serializers
from ..models import User, Address, Category, Product, Inventory, Offer, Cart, CartItem, Order, OrderItem, Payment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'mobile_number', 'role', 'status']

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'price']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    class Meta:
        model = Cart
        fields = ['id', 'items']

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'unit_price', 'total_price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    payment = serializers.SerializerMethodField()
    class Meta:
        model = Order
        fields = ['id', 'user', 'address', 'total_amt', 'status', 'items', 'payment']

    def get_payment(self, obj):
        if hasattr(obj, 'payment'):
            return PaymentSerializer(obj.payment).data
        return None

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'