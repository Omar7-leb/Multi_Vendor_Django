import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import include, path




urlpatterns = [
    path('secret/', admin.site.urls),
    path('', include('core.urls')),
    path('blog/', include('blog.urls')),
    path('vendor/', include('vendor.urls')),
    path('customer/', include('customers.urls')),
    path('product/', include('product.urls')),
    path('category/', include('product.urls')),
    path('cart/', include('cart.urls')),
    path('wishlist/', include('wishlist.urls')),
    path('order/', include('order.urls')),
    path('review/', include('review.urls')),
    path('newsletter/', include('newsletter.urls')),
    path('__debug__/', include(debug_toolbar.urls)),
    path('api/', include('api.urls')),
    path('search/', include('elasticsearchdjgo.urls')),
    path('chat/', include('chat.urls')),
    path('image_search/', include('imageSearch.urls')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
