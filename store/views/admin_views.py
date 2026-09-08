from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from ..models import User  # <--- Use the Custom User from your models


from ..services import admin_service, catalog_service
from ..models import Product, Order, Category, Offer
from ..serializers import ProductSerializer, CategorySerializer, OrderSerializer, UserSerializer
from ..serializers.admin_serializers import AdminOrderStatusUpdateSerializer, AdminUserUpdateSerializer

class AdminDashboardStatsView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        stats = admin_service.get_dashboard_stats()
        return Response(stats)

class AdminCategoryListCreateView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        categories = catalog_service.admin_get_categories()
        return Response(CategorySerializer(categories, many=True).data)
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            category = catalog_service.admin_create_category(serializer.validated_data)
            return Response(CategorySerializer(category).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdminCategoryUpdateDeleteView(APIView):
    permission_classes = [IsAdminUser]
    def put(self, request, pk):
        serializer = CategorySerializer(data=request.data, partial=True)
        if serializer.is_valid():
            category = catalog_service.admin_update_category(pk, serializer.validated_data)
            return Response(CategorySerializer(category).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk):
        catalog_service.admin_delete_category(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

class AdminProductListCreateView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        products = catalog_service.admin_get_products()
        return Response(ProductSerializer(products, many=True).data)
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = catalog_service.admin_create_product(serializer.validated_data)
            return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdminProductUpdateDeleteView(APIView):
    permission_classes = [IsAdminUser]
    def put(self, request, pk):
        serializer = ProductSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            product = catalog_service.admin_update_product(pk, serializer.validated_data)
            return Response(ProductSerializer(product).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk):
        catalog_service.admin_delete_product(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

class AdminOrderListView(ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

class AdminOrderStatusUpdateView(APIView):
    permission_classes = [IsAdminUser]
    def put(self, request, pk):
        serializer = AdminOrderStatusUpdateSerializer(data=request.data)
        if serializer.is_valid():
            order = admin_service.admin_update_order_status(pk, serializer.validated_data['status'])
            return Response(OrderSerializer(order).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdminUserListView(ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.all()

class AdminUserUpdateView(APIView):
    permission_classes = [IsAdminUser]
    def put(self, request, pk):
        user = User.objects.get(id=pk)
        serializer = AdminUserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(UserSerializer(user).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)