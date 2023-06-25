from django.shortcuts import render
import sys
from os.path import dirname, abspath
from django.db.models import Q
from rest_framework.decorators import api_view

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

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
from order.models import  Order, OrderItem
from .serializers.messageSerializers import *
from chat.models import Message
from .serializers.vendorSerializers import *

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

class GetProductDetails(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ProductDetailsSerializer
    def get_queryset(self):
        product_id = self.kwargs["pk"]
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


class AddOrder(generics.CreateAPIView):
    queryset = Order.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = OrderSerializer



class AddToWishList(generics.UpdateAPIView):
    queryset = Product.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = WishListSerializer

class GetWishList(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ProductSimpleSerializer

    def get_queryset(self):
        customer_id = self.kwargs["customer_id"]
        return  Product.objects.filter(wishlist=customer_id)




class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        if user.is_customer:
            token['customer'] = user.customer.id

        if user.is_vendor:
            token['vendor'] = user.vendor.id

        token['email'] = user.email

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer



class GetRoomsView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = GetRoomSerializer

    def get_queryset(self):
        vendor_id = self.kwargs["pk"]
        rooms = Message.objects.filter(Q(receiver=vendor_id) | Q(sender=vendor_id)).values('room_name').distinct()
        print(rooms)
        result = []

        for room in rooms:
            data = {}
            last_message = Message.objects.filter(room_name=room["room_name"]).latest("timestamp")
            data["last_message"] = last_message.content
            data["room_name"] = last_message.room_name
            if last_message.sender.is_customer:
                data["customer"] = last_message.sender.email
            else:
                data["customer"] = last_message.receiver.email

            data["timestamp"] = last_message.timestamp

            result.append(data)
        print(result)
        return result


class GetMessagesView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = GetMessageSerializer

    def get_queryset(self):
        room_name = self.kwargs["room_name"]
        return Message.objects.filter(room_name=room_name)

class RegisterVendorView(generics.CreateAPIView):
    queryset = Customer.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = VendorSerializer


class GetOrderItems(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = GetOrderItemSerializer

    def get_queryset(self):
        order_id = self.kwargs["order_id"]
        return OrderItem.objects.filter(order=order_id)


class GetOrders(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = GetOrderSerializer

    def get_queryset(self):
        customer_id = self.kwargs["customer_id"]
        return Order.objects.filter(customer=customer_id)

