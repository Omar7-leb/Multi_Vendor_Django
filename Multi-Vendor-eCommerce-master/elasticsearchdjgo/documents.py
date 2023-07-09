# documents.py

from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from product.models import Product


@registry.register_document
class ProductDocument(Document):
    slug = fields.TextField(attr="get_slug")

    created_by = fields.ObjectField(properties={
        'vendor_name': fields.TextField(),
        'coordinates': fields.GeoPointField(attr="location_field_indexing")
    })

    category = fields.ObjectField(properties={
        'name':fields.TextField(),
        "slug":fields.TextField(attr="get_slug")
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

