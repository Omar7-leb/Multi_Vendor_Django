from django.shortcuts import render
import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers.customerSerializers import CustomerSerializer
from .serializers.productSerializers import *
from .serializers.addProductSerializers import *
from rest_framework import status
from customers.models import Customer
from product.models import Product, Category, CategoryOptions, CategoryProductOptions

# Create your views here.
class RegisterCustomerView(generics.CreateAPIView):
    queryset = Customer.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = CustomerSerializer


class AddProduct(generics.CreateAPIView):
    queryset = Product.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = AddProductSerializer

class GetProductsView(generics.ListAPIView):
    queryset = Product.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ProductSimpleSerializer


class GetVendorProductsView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ProductSimpleSerializer

    def get_queryset(self):
        vendor_id = self.kwargs["vendor_id"]
        return Product.objects.filter(created_by=vendor_id)

class GetProductDetails(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ProductDetailsSerializer
    def get_queryset(self):
        product_id = self.kwargs["product_id"]
        return Product.objects.filter(id=product_id)


class GetCategories(generics.ListAPIView):
    queryset = Category.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = CategorySerializer


class GetCategoryOptions(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = CategoryOptionsSerializer

    def get_queryset(self):
        category_id = self.kwargs["category_id"]
        return CategoryOptions.objects.filter(category=category_id)


class AddCategoryOption(generics.CreateAPIView):
    queryset = CategoryOptions.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = CategoryOptionsSerializer

class AddCategoryProductOptions(APIView):
    def post(self, request, format=None):
        serializer = CategoryProductOptionsSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

