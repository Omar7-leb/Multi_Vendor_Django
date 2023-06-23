from rest_framework import serializers
from order.models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'order', 'customer', 'vendor', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'first_name', 'last_name', 'email', 'address', 'zipcode', 'place',
                  'phone', 'paid_amount', 'total_price', 'isPaid', 'paid_date', 'isDelivered',
                  'delivered_date', 'isCancelled', 'isReturn', 'order_created', 'customer',
                  'status', 'order_items']
