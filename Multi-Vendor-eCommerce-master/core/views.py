from django.contrib import messages
from django.db.models import Q
from django.http import Http404, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.cache import cache_page
from product.models import Product, Category
from django.shortcuts import get_object_or_404

from .models import Contact


def home(request):
    products = Product.objects.all()
    return render(request, 'core/home.html', {'products': products})


def latest(request):
    products = Product.objects.all()
    return render(request, 'core/latest.html', {'products': products})


def products(request):
    sort_option = request.GET.get('sort', None)
    if sort_option == 'featured-rank':
        products = Product.objects.filter()
    elif sort_option == 'price_asc':
        products = Product.objects.order_by('price')
    elif sort_option == 'price_desc':
        products = Product.objects.order_by('-price')
    elif sort_option == 'review-rank':
        products = Product.objects.order_by('-is_review')
    elif sort_option == 'date-desc-rank':
        products = Product.objects.order_by('-is_new', '-created_at')
    else:
        products = Product.objects.all()
    return render(request, 'core/products.html', {'products': products})


def category_products(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
        products = category.product_set.all()
    except Category.DoesNotExist:
        category = None
        products = []

    context = {
        'category': category,
        'products': products
    }
    return render(request, 'core/category.html', context)


@cache_page(60 * 60)
def search_api(request):
    ''' Search API for autocomplete '''
    queryset = request.GET.get('query')
    if queryset:
        products = Product.objects.filter(Q(title__icontains=queryset) | Q(
            slug__icontains=queryset) | Q(description__icontains=queryset))
        jsonPayload = []
        for product in products:
            jsonPayload.append({
                'title': product.title,
                'slug': product.slug,
                # 'image': print(type(product.image)),
                'url': product.url,
                'description': product.description,
            })

        return JsonResponse({
            'status': 200,
            'data': jsonPayload
        })
    else:
        raise Http404


@cache_page(60 * 60)
def search(request):
    ''' redirect search result  '''
    queryset = request.GET.get('query')
    if queryset:
        products = Product.objects.filter(Q(title__icontains=queryset) | Q(
            slug__icontains=queryset) | Q(description__icontains=queryset))
        return render(request, 'core/search.html', {'results': products})
    else:
        raise Http404


def about(request):
    return render(request, 'core/about.html')


def contact(request):
    '''
    user contact submission form
    '''
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        subject = request.POST.get('subject')
        contact = Contact(name=name, email=email, message=message, subject=subject)
        contact.save()
        messages.success(request, 'Your message has been sent successfully')
        return redirect('contact')

    return render(request, 'core/contact.html')
