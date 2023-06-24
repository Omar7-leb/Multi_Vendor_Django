from autoslug import AutoSlugField
from cloudinary.models import CloudinaryField
from taggit.managers import TaggableManager

from customers.models import Customer
from django.db import models
from model.common_fields import BaseModel
from vendor.models import Vendor
from django.http import HttpRequest


class Category(models.Model):
    """ Category model """
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='name')

    # category_image = models.ImageField(upload_to='category_images')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']


class Product(BaseModel):
    """ Product model """
    title = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='title')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    SIZE_CHOICE = (
        ("m", "M"),
        ("l", "L"),
        ("xl", "XL"),
    )
    size = models.CharField(
        max_length=10, choices=SIZE_CHOICE, null=True, blank=True)
    image = models.ImageField(upload_to='product/', null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    available = models.BooleanField(default=True)
    is_new = models.BooleanField(default=False)
    is_review = models.BooleanField(default=False)

    rating = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True)
    numbersOfReview = models.IntegerField(null=True, blank=True, default=0)
    countInStock = models.IntegerField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_by = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, related_name="customer", on_delete=models.CASCADE, null=True)
    wishlist = models.ManyToManyField(Customer)

    tags = TaggableManager()

    def __str__(self):
        return self.title

    def wishlist_exist(self, customer_id):
        '''
        Check if the product is in the wishlist
        '''

        return self.wishlist.filter(id=customer_id).exists()

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except Exception:
            url = ""
        return url

    class Meta:
        verbose_name_plural = 'Products'


class CategoryOptions(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='options')
    name = models.CharField(max_length=255)

    # Add other fields as needed

    def __str__(self):
        return self.name


class CategoryProductOptions(models.Model):
    category_option = models.ForeignKey(CategoryOptions, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    value = models.TextField(max_length=30)

