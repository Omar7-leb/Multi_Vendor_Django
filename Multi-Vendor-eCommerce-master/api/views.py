from django.shortcuts import render
import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))

from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers.customerSerializers import CustomerSerializer
from .serializers.productSerializers import ProductSimpleSerializer, ProductDetailsSerializer
from .serializers.addProductSerializers import *

from customers.models import Customer
from product.models import Product, Category, CategoryOptions

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
        return CategoryOptions.objects.filter(id=category_id)


class AddCategoryOption(generics.CreateAPIView):
    queryset = CategoryOptions  .objects.all()
    permission_classes = (AllowAny,)
    serializer_class = CategoryOptionsSerializer