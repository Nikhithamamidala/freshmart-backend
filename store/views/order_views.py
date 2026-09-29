from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.utils import timezone
from rest_framework import status
from ..models import Order, OrderItem, Cart, Payment, Address
from ..serializers import OrderSerializer


# 7. CHECKOUT MODULE
class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        cart = get_object_or_404(Cart, user=request.user)

        if not cart.items.exists():
            return Response({"error": "Cart is empty"}, status=400)

        # Step 1: Create the Address from the checkout form data
        address = Address.objects.create(
            user=request.user,
            full_name=request.data.get('full_name', ''),
            phone=request.data.get('mobile_number', ''),
            address=request.data.get('shipping_address', ''),
            city=request.data.get('city', ''),
            state=request.data.get('state', ''),
            pincode=request.data.get('pincode', '')
        )

        # Step 2: Calculate total, check stock, and prepare items
        total = 0
        order_items_data = []

        for item in cart.items.all():
            # NOTE: New field name is stock_quantity (not stock)
            if item.product.stock_quantity < item.quantity:
                return Response(
                    {"error": f"Insufficient stock for {item.product.product_name}"},
                    status=400
                )

            item_total = item.product.price * item.quantity
            total += item_total

            order_items_data.append({
                'product': item.product,
                'quantity': item.quantity,
                'unit_price': item.product.price,
                'total_price': item_total
            })

            # Deduct stock (new field name)
            item.product.stock_quantity -= item.quantity
            item.product.save()

        # Step 3: Create the Order (new field names: address, total_amt)
        order = Order.objects.create(
            user=request.user,
            address=address,
            total_amt=total,
            status='pending'
        )

        # Step 4: Create OrderItems
        for data in order_items_data:
            OrderItem.objects.create(order=order, **data)

        # Step 5: Clear the cart
        cart.items.all().delete()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


# 8. PAYMENT MODULE
class PaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        order = get_object_or_404(
            Order,
            id=request.data.get('order_id'),
            user=request.user
        )
        payment, created = Payment.objects.get_or_create(
            order=order,
            defaults={
                'payment_status': 'paid',
                'transaction_id': 'MOCK-TXN-123',
                'paid_at': timezone.now(),
                'payment_method': request.data.get('payment_method', 'COD'),
                'amount': order.total_amt
            }
        )
        if not created:
            payment.payment_status = 'paid'
            payment.save()

        order.status = 'processing'
        order.save()

        return Response({
            "message": "Payment Successful!",
            "order_id": order.id,
            "status": order.status
        })


# 9. MY ORDERS & DETAILS
class OrderList(ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderDetail(RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)