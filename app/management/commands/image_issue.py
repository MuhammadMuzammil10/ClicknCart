import json , os , requests
from django.core.management.base import BaseCommand
from app.models import Product , Category , Brand , Product_images
from django.core.files import File
class Command(BaseCommand):
    help = 'Import products from a JSON file'

    def handle(self, *args, **options):
        # for i in range(141, 166):
        #     product = Product.objects.get(id = i)
        #     try:
        #         product_images = Product_images.objects.filter(product = product)
        #         print(product_images , 'product_images')
        #         if product_images:
        #             product_images.first().delete()
        #             print(product_images)
        #     except Product_images.DoesNotExist:
        #         print("does not exist for " , product)
        product = Product.objects.filter(category__name__iexact = 'nursery')[15:]
        # print(product.delete)
        print(product.count())
        
        