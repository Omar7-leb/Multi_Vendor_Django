from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from cloudinary.forms import CloudinaryFileField
from django_countries.fields import CountryField

from customers.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms import ModelForm
from product.models import Product

from .models import Vendor


class VendorSignUpForm(UserCreationForm):
    country = CountryField(blank_label='(Select country)').formfield(null=True, widget=forms.Select(attrs={'id': 'id_country'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))
    mobile_number = forms.CharField(max_length=17)
    vendor_name = forms.CharField(max_length=255)
    shop_logo = forms.ImageField()
    owner_name = forms.CharField(max_length=255)
    nid_number = forms.CharField(max_length=10)
    #latitude = forms.FloatField(widget=forms.HiddenInput(), required=False)
    #longitude = forms.FloatField(widget=forms.HiddenInput(), required=False)
    latitude = forms.FloatField(required=False)
    longitude = forms.FloatField(required=False)
    def __init__(self, *args, **kwargs):
        super(VendorSignUpForm, self).__init__(*args, **kwargs)

        for fieldname in ["password1", "password2"]:
            self.fields[fieldname].help_text = None

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            'owner_name', 'email', 'mobile_number', 'nid_number', 'vendor_name',
            'shop_logo', 'country', 'address', 'password1', 'password2'
        )

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_vendor = True
        user.save()
        vendor = Vendor.objects.create(user=user)
        vendor.owner_name = self.cleaned_data.get('owner_name')
        vendor.email = self.cleaned_data.get('email')
        vendor.mobile_number = self.cleaned_data.get('mobile_number')
        vendor.nid_number = self.cleaned_data.get('nid_number')
        vendor.vendor_name = self.cleaned_data.get('vendor_name')
        vendor.shop_logo = self.cleaned_data.get('shop_logo')
        vendor.country = self.cleaned_data.get('country')
        vendor.address = self.cleaned_data.get('address')
        vendor.latitude = self.cleaned_data.get('latitude')
        vendor.longitude = self.cleaned_data.get('longitude')
        vendor.save()
        return vendor


class ProductForm(ModelForm):

    class Meta:
        model = Product
        fields = ('title', 'category', 'price', 'description', 'countInStock',
                  'size', 'image', 'available')
        labels = {
            'title': 'Title',
            'category': 'Category',
            'price': 'Price',
            'description': 'Description',
            'countInStock': 'In Stock',
            'size': 'Size',
            'image': 'Image',
            'available': 'Available',
        }
