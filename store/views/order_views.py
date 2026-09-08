from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.utils import timezone
from rest_framework import status
from ..models import Order, OrderItem, Cart, Payment
from ..serializers import OrderSerializer

# 7. CHECKOUT MODULE
class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]
    @transaction.atomic
    def post(self, request):
        cart = get_object_or_404(Cart, user=request.user)
        if not cart.items.exists(): return Response({"error": "Cart is empty"}, status=400)
        
        total = 0
        order_items_data = []
        
        for item in cart.items.all():
            if item.product.stock < item.quantity: return Response({"error": f"Insufficient stock for {item.product.name}"}, status=400)
            total += item.product.price * item.quantity
            order_items_data.append({'product': item.product, 'quantity': item.quantity, 'price_at_purchase': item.product.price})
            # Deduct stock
            item.product.stock -= item.quantity
            item.product.save()
            
        # ⭐ UPDATED LINE BELOW: Added full_name and mobile_number from the frontend data
        order = Order.objects.create(
            user=request.user, 
            full_name=request.data.get('full_name', ''), 
            mobile_number=request.data.get('mobile_number', ''), 
            shipping_address=request.data['shipping_address'], 
            payment_method=request.data['payment_method'], 
            total_amount=total, 
            final_amount=total
        )
        
        for data in order_items_data: OrderItem.objects.create(order=order, **data)
        cart.items.all().delete()
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

# 8. PAYMENT MODULE
class PaymentView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        order = get_object_or_404(Order, id=request.data.get('order_id'), user=request.user)
        payment, created = Payment.objects.get_or_create(order=order, defaults={'payment_status': 'paid', 'transaction_id': 'MOCK-TXN-123', 'paid_at': timezone.now()})
        if not created: payment.payment_status = 'paid'; payment.save()
        order.status = 'processing'
        order.save()
        return Response({"message": "Payment Successful!", "order_id": order.id, "status": order.status})

# 9. MY ORDERS & DETAILS
class OrderList(ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self): return Order.objects.filter(user=self.request.user)

class OrderDetail(RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self): return Order.objects.filter(user=self.request.user)