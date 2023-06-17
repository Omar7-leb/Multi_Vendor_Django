from rest_framework import serializers
from os.path import dirname, abspath
import sys
sys.path.append(dirname(dirname(abspath(__file__))))

from customers.models import *




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password"]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.is_customer = True
        user.save()

        return user


class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Customer
        fields = ['user', 'full_name', 'phone_number', 'address', 'country']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = UserSerializer(data=user_data)
        user = None

        if user_serializer.is_valid():
            user = user_serializer.save()

        full_name = validated_data.get("full_name")
        email = user_data.get("email")
        country = validated_data.get("country")
        phone_number = validated_data.get("phone_number")
        address = validated_data.get("address")

        customer = Customer(full_name=full_name, email=email, country=country, phone_number=phone_number, address=address,
                            user=user)
        customer.save()

        return customer
