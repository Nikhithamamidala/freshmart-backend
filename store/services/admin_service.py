from django.contrib.auth.models import User
from ..models import Product, Order, Category, Offer
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta

def get_dashboard_stats():
    total_sales = Order.objects.filter(status__in=['processing', 'shipped', 'delivered']).aggregate(total=Sum('final_amount'))['total'] or 0
    total_orders = Order.objects.count()
    total_products = Product.objects.count()
    total_customers = User.objects.filter(is_staff=False).count()

    seven_days_ago = timezone.now() - timedelta(days=7)
    recent_orders = Order.objects.filter(created_at__gte=seven_days_ago)

    sales_chart = []
    for i in range(7):
        day = seven_days_ago + timedelta(days=i)
        day_sales = recent_orders.filter(created_at__date=day.date()).aggregate(total=Sum('final_amount'))['total'] or 0
        sales_chart.append({'date': day.strftime('%b %d'), 'sales': day_sales})

    status_counts = {
        'pending': Order.objects.filter(status='pending').count(),
        'processing': Order.objects.filter(status='processing').count(),
        'shipped': Order.objects.filter(status='shipped').count(),
        'delivered': Order.objects.filter(status='delivered').count(),
        'cancelled': Order.objects.filter(status='cancelled').count(),
    }

    return {
        'total_sales': total_sales,
        'total_orders': total_orders,
        'total_products': total_products,
        'total_customers': total_customers,
        'sales_chart': sales_chart,
        'status_counts': status_counts
    }

def admin_update_order_status(order_id, new_status):
    order = Order.objects.get(id=order_id)
    order.status = new_status
    order.save()
    return order