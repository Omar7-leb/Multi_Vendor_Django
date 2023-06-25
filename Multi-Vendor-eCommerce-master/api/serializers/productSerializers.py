from rest_framework import serializers
from product.models import Product
from order.models import Order, OrderItem


class ProductSimpleSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.vendor_name')

    class Meta:
        model = Product
        fields = ["id", "title", "description", "price", "discount", "image", "rating", "created_by", "available"]


class ProductDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["product", "quantity", "price"]

    def create(self, validated_data):
        quantity = validated_data.pop('quantity')
        price = validated_data.pop('price')

        order = self.context['order_id']
        product = self.context['product_id']

        order_item = OrderItem(product=product, order=order, price=price, quantity=quantity)
        order_item.save()

        return order_item


class OrderSerializer(serializers.ModelSerializer):
    orderItem = OrderItemSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = ["customer", "orderItem"]

    def create(self, validated_data):
        customer = validated_data.get("customer")

        order = Order(customer=customer)
        order.save()


        print("working")
        order_items = validated_data.pop('orderItem')

        for order_item in order_items:
            product = order_item.pop("product")

            order_item_serializer = OrderItemSerializer(data=order_item,
                                                        context={'order_id': order, 'product_id': product})
            if order_item_serializer.is_valid():
                order_item_serializer.save()
            else:
                print(order_item_serializer.errors)

        return order


class WishListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['wishlist']

    def update(self, instance, validated_data):
        wishlist = validated_data.pop("wishlist")

        for user in wishlist:
            if not instance.wishlist.filter(id=user.id).exists():
                instance.wishlist.add(user.id)
            else:
                instance.wishlist.remove(user.id)

        return instance


class GetOrderItemSerializer(serializers.ModelSerializer):
    product = ProductSimpleSerializer()
    class Meta:
        model = OrderItem
        fields = ["product", "quantity", "price"]


class GetOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "order_created", "total_price"]

