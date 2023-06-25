from rest_framework import serializers
from vendor.models import Vendor
from customers.models import User

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
        user.is_vendor = True
        user.save()

        return user


class VendorSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Vendor
        fields = ['user', 'vendor_name', 'mobile_number', 'address', 'latitude', 'longitude']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = UserSerializer(data=user_data)
        user = None

        if user_serializer.is_valid():
            user = user_serializer.save()

        vendor_name = validated_data.get("vendor_name")
        mobile_number = validated_data.get("mobile_number")
        address = validated_data.get("address")
        latitude = validated_data.get("latitude")
        longitude = validated_data.get("longitude")

        vendor = Vendor(vendor_name=vendor_name, mobile_number=mobile_number, address=address,
                        user=user, latitude=latitude, longitude=longitude)
        vendor.save()

        return vendor