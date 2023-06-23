from django.shortcuts import render, get_object_or_404
from vendor.models import Vendor
from product.models import Product


def vendor_products(request, vendor_id):
    # Retrieve the vendor based on the vendor_id
    vendor = get_object_or_404(Vendor, id=vendor_id)

    # Fetch the list of products associated with the vendor
    products = Product.objects.filter(created_by=vendor)

    # Pass the vendor and products to the template context
    context = {
        'vendor': vendor,
        'products': products,
    }
    return render(request, 'vendor/vendor_products.html', context)


