from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.db import transaction
from ..models import Cart, CartItem, Product, Address, Order, OrderItem
from ..serializers import CartSerializer, OrderSerializer
from ..services import order_service

# 6. CART MODULE
class CartView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return Response(CartSerializer(cart).data)

    def post(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        product = get_object_or_404(Product, id=request.data.get('product_id'))
        quantity = int(request.data.get('quantity', 1))
        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created: 
            item.quantity += quantity
        else: 
            item.quantity = quantity
        item.price = product.price * item.quantity
        item.save()
        return Response(CartSerializer(cart).data, status=status.HTTP_201_CREATED)

class CartItemUpdateDelete(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, pk):
        item = get_object_or_404(CartItem, pk=pk, cart__user=request.user)
        item.quantity = int(request.data.get('quantity', 1))
        item.price = item.product.price * item.quantity
        item.save()
        return Response(CartSerializer(item.cart).data)
        
    def delete(self, request, pk):
        item = get_object_or_404(CartItem, pk=pk, cart__user=request.user)
        item.delete()
        return Response(CartSerializer(item.cart).data)

# 7. CHECKOUT MODULE
class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]
    @transaction.atomic
    def post(self, request):
        try:
            # Use the order_service logic we wrote earlier
            order = order_service.checkout(
                user=request.user,
                address_id=request.data.get('address_id'),
                items_data=request.data.get('items')
            )
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)