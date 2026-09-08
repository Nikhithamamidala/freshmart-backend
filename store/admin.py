from django.contrib import admin
from .models import User, Address, Category, Product, Inventory, Offer, Cart, CartItem, Order, OrderItem, Payment

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'mobile_number', 'role', 'status')
    search_fields = ('username', 'email')

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'city', 'state', 'pincode')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'status')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'unit', 'stock_quantity', 'category', 'status')
    list_filter = ('category', 'status')
    list_editable = ('price', 'stock_quantity')
    search_fields = ('product_name',)

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'opening_stock', 'purchased', 'sold_stock', 'remaining', 'low_stock_limit')

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('offer_code', 'offer_type', 'discount', 'minimum_order', 'status')
    list_filter = ('offer_type', 'status')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'address', 'total_amt', 'status')
    list_filter = ('status',)
    inlines = [OrderItemInline]
    readonly_fields = ('user', 'address', 'total_amt')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'unit_price', 'total_price')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'price')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'payment_method', 'amount', 'payment_status', 'payment_date')
    list_filter = ('payment_status', 'payment_method')