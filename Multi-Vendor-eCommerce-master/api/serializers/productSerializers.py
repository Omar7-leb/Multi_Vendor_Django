from rest_framework import serializers
from product.models import Product

class ProductSimpleSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.vendor_name')
    class Meta:
        model = Product
        fields = ["title", "description", "price", "discount", "image", "rating", "created_by"]


class ProductDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = "__all__"



