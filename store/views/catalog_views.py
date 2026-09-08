from django.http import JsonResponse
from rest_framework import generics
from rest_framework.permissions import AllowAny
from ..models import Product, Category
from ..serializers import ProductSerializer, CategorySerializer

# 1. HOME PAGE
def home(request):
    return JsonResponse({"message": "Welcome to FreshMart Backend API!", "status": "Running"})

# 2. CATEGORY LISTING
class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

# 3. VEGETABLES LISTING
class ProductList(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    def get_queryset(self):
        queryset = Product.objects.all()
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__name=category)
        return queryset

# 4. VEGETABLE DETAILS
class ProductDetail(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]