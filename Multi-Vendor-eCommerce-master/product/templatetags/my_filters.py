from django import template

register = template.Library()

@register.filter
def wishlist_exists(product, customer_id):
    '''
    Check if the product is in the wishlist of the specified customer
    '''
    return product.wishlist.filter(id=customer_id).exists()