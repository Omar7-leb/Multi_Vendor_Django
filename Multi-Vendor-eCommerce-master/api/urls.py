from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from .views import *

urlpatterns=[
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('add_customer/', RegisterCustomerView.as_view(), name="register_customer"),
    path("get_products/", GetProductsView.as_view(), name="get_products"),
    path("get_product_details/<int:product_id>/", GetProductDetails.as_view(), name="get_product_details")
]