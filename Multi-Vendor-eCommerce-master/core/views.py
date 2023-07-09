from django.contrib import messages
from django.http import Http404, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.cache import cache_page
from product.models import Product, Category
from vendor.models import Vendor
from django.shortcuts import get_object_or_404

from elasticsearchdjgo.search import lookup
from elasticsearchdjgo.documents import ProductDocument

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl import Q

from .models import Contact
import requests


def home(request):
    products = Product.objects.all()
    return render(request, 'core/home.html', {'products': products})


def latest(request):
    products = Product.objects.all()
    return render(request, 'core/latest.html', {'products': products})


def products(request):
    categories = Category.objects.all()
    vendors = Vendor.objects.all()

    q = []

    client = Elasticsearch()

    category = request.GET.get('category')
    min_price = request.GET.get("min")
    max_price = request.GET.get("max")
    vendor = request.GET.get("vendor")
    available = request.GET.get("available")
    location = request.GET.get("location")

    if category != "None" and category is not None:
        q.append(Q(
            'multi_match',
            query=category,
            fields=[
                'category.name'
            ])
        )

    if vendor != "None" and vendor is not None:
        q.append(Q(
            'multi_match',
            query=vendor,
            fields=[
                'created_by.vendor_name'
            ])
        )

    if max_price:
        q.append(Q('range', price={'lte': max_price}))

    if min_price:
        q.append(Q('range', price={"gte": min_price}))

    if available == "on":
        q.append(Q('match', available=True))

    if location:
        location = city_name_to_lat_long(location)
        q.append(Q("geo_distance", distance="2km", created_by__coordinates={"lat": location['latitude'],
                                                                            "lon": location['longitude']}))

    if not q:
        q.append(Q('match_all'))

    final_q = Q(
        'bool',
        must=q
    )
    s = Search().using(client).query(final_q)

    response = s.execute()

    product = responseToOject(response)
    print(product)

    # sort_option = request.GET.get('sort', None)
    # if sort_option == 'featured-rank':
    #     products = Product.objects.filter()
    # elif sort_option == 'price_asc':
    #     products = Product.objects.order_by('price')
    # elif sort_option == 'price_desc':
    #     products = Product.objects.order_by('-price')
    # elif sort_option == 'review-rank':
    #     products = Product.objects.order_by('-is_review')
    # elif sort_option == 'date-desc-rank':
    #     products = Product.objects.order_by('-is_new', '-created_at')
    # else:
    #     products = Product.objects.all()

    return render(request, 'core/products.html', {'products': product, 'categories': categories, 'vendors': vendors})


def category_products(request, category_id):
    category = Category.objects.get(id=category_id)

    sort_option = request.GET.get('sort', None)
    if sort_option == 'featured-rank':
        products = Product.objects.filter(category=category)
    elif sort_option == 'price_asc':
        products = Product.objects.filter(category=category).order_by('price')
    elif sort_option == 'price_desc':
        products = Product.objects.filter(category=category).order_by('-price')
    elif sort_option == 'review-rank':
        products = Product.objects.filter(category=category).order_by('-is_review')
    elif sort_option == 'date-desc-rank':
        products = Product.objects.filter(category=category).order_by('-is_new', '-created_at')
    else:
        products = Product.objects.filter(category=category)

    context = {
        'category': category,
        'products': products,
    }

    return render(request, 'core/category.html', context)


# @cache_page(60 * 60)
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


# @cache_page(60 * 60)
def search(request):
    ''' redirect search result  '''
    queryset = request.GET.get('query')
    if queryset:
        products = lookup(query=queryset)
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


def city_name_to_lat_long(city):
    api_url = "https://api.api-ninjas.com/v1/geocoding?city={}&country=Lebanon".format(city)
    response = requests.get(api_url + city, headers={'X-Api-Key': 'dsHO59gahSzrqPVqRbp8RQ==Gpzt4v3istbe4Epc'})
    if response.status_code == requests.codes.ok:
        data = response.json()
        result = filter(lambda x: x['country'] == "LB", data)
        return list(result)[0]
    else:
        print("Error:", response.status_code, response.text)


def responseToOject(response):
    result = []
    for hit in response:
        data = {
            "id": hit.id,
            "title": hit.title,
            "description": hit.description,
            "created_by": hit.created_by.vendor_name,
            "image": hit.image,
            "price": hit.price,
            "category_slug": hit.category.slug,
            "slug": hit.slug
        }

        ws = []
        for w in hit.wishlist:
            ws.append(w["id"])

        data["wishlist"] = ws
        result.append(data)

    return result
