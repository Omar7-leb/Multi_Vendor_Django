from django.urls import include,path
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'customers', CustomerViewSet)

urlpatterns=[
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('add_customer/', RegisterCustomerView.as_view(), name="register_customer"),
    path("get_products/", GetProductsView.as_view(), name="get_products"),
    path("get_product_details/<int:pk>/", GetProductDetails.as_view(), name="get_product_details"),
    path("add_product/", AddProduct.as_view(), name="add_product"),
    path("get_vendor_products/<int:vendor_id>/",GetVendorProductsView.as_view(),name="get_vendor_products"),
    path("get_categories/", GetCategories.as_view(), name="get_categories"),
    path("get_category_options/<int:category_id>/", GetCategoryOptions.as_view(), name="get_category_options"),
    path("add_category_option/", AddCategoryOption.as_view(), name ="add_category_option"),
    path("add_product_categoryOptions/", AddCategoryProductOptions.as_view(), name="add_product_categoryOptions"),
    path("get_orders/", OrderItemListCreateView.as_view(), name="get_orders"),
    path('profile/', include(router.urls))
]