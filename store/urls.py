from django.urls import path
from .views import catalog_views, auth_views, cart_views, order_views, admin_views

urlpatterns = [
    # Home Page
    path('', catalog_views.home, name='home'),

    # Auth
    path('api/users/register/', auth_views.RegisterView.as_view(), name='register'),
    path('api/users/login/', auth_views.LoginView.as_view(), name='login'),
    path('api/users/profile/', auth_views.UserProfileView.as_view(), name='profile'),

    # Catalog (Vegetables & Categories)
    path('api/categories/', catalog_views.CategoryList.as_view(), name='category-list'),
    path('api/products/', catalog_views.ProductList.as_view(), name='product-list'),
    path('api/products/<int:pk>/', catalog_views.ProductDetail.as_view(), name='product-detail'),

    # Cart
    path('api/cart/', cart_views.CartView.as_view(), name='cart'),
    path('api/checkout/', cart_views.CheckoutView.as_view(), name='checkout'),
    path('api/cart/items/<int:pk>/', cart_views.CartItemUpdateDelete.as_view(), name='cart-item-update'),

    # Checkout, Payment & Orders
    path('api/checkout/', order_views.CheckoutView.as_view(), name='checkout'),
    path('api/payment/', order_views.PaymentView.as_view(), name='payment'),
    path('api/orders/', order_views.OrderList.as_view(), name='order-list'),
    path('api/orders/<int:pk>/', order_views.OrderDetail.as_view(), name='order-detail'),

    # Admin Dashboard
    path('api/admin/stats/', admin_views.AdminDashboardStatsView.as_view(), name='admin-stats'),
    path('api/admin/categories/', admin_views.AdminCategoryListCreateView.as_view(), name='admin-category-list'),
    path('api/admin/categories/<int:pk>/', admin_views.AdminCategoryUpdateDeleteView.as_view(), name='admin-category-detail'),
    path('api/admin/products/', admin_views.AdminProductListCreateView.as_view(), name='admin-product-list'),
    path('api/admin/products/<int:pk>/', admin_views.AdminProductUpdateDeleteView.as_view(), name='admin-product-detail'),
    path('api/admin/orders/', admin_views.AdminOrderListView.as_view(), name='admin-orders'),
    path('api/admin/orders/<int:pk>/', admin_views.AdminOrderStatusUpdateView.as_view(), name='admin-order-status'),
    path('api/admin/users/', admin_views.AdminUserListView.as_view(), name='admin-users'),
    path('api/admin/users/<int:pk>/', admin_views.AdminUserUpdateView.as_view(), name='admin-user-update'),
]