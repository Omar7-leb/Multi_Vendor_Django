from django.shortcuts import render
from vendor.models import Vendor


def vendor_list(request):
    vendors = Vendor.objects.all()
    context = {'vendors': vendors}
    return render(request, 'vendor/list_vendors.html', context)
