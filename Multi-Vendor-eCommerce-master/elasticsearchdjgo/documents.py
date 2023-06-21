# documents.py

from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from product.models import Product


@registry.register_document
class ProductDocument(Document):
    created_by = fields.ObjectField(properties={
        'vendor_name': fields.TextField()
    })

    category = fields.ObjectField(properties={
        'name':fields.TextField()
    })

    wishlist = fields.NestedField(properties={
        'id': fields.IntegerField()
    })
    class Index:
        name = 'products'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Product

        fields = [
            "id",
            "title",
            "description",
            "price",
            "discount",
            "image",
            "rating",
            "available",
        ]

