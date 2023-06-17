from rest_framework import serializers
from product.models import Product, CategoryProductOptions, Category, CategoryOptions
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class CategoryOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryOptions
        fields = "__all__"

class CategoryProductOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryProductOptions
        fields = ["product","category_option", "value"]


class AddProductSerializer(serializers.ModelSerializer):
    # category_options = CategoryProductOptionsSerializer(many=True, write_only=True)
    class Meta:
        model = Product
        fields = ["id","title", "description", "price", "image", "countInStock","created_by", "category"]
                  # "category_options"]

    # def create(self, validated_data):
    #     options_data = validated_data.pop('category_options')
    #     product = Product.objects.create(**validated_data)
    #
    #     # for option_data in options_data:
    #     #     product_option_serializer = CategoryProductOptionsSerializer(data=option_data, context={'product_id': product})
    #     #     if product_option_serializer.is_valid():
    #     #         product_option_serializer.save()
    #
    #     return product