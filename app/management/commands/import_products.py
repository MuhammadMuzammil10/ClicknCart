import json , os , requests
from django.core.management.base import BaseCommand
from app.models import Product , Category , Brand , Product_images
from django.core.files import File
class Command(BaseCommand):
    help = 'Import products from a JSON file'

    def handle(self, *args, **options):
        file_name = 'img_product.json'  # Specify the file name
        current_directory = os.path.dirname(os.path.abspath(__file__))
        json_file_path = os.path.join(current_directory, file_name)
        with open(json_file_path, 'r') as file:
            products_data = json.load(file)
            # print(products_data , 'product_data')
            for product_data in products_data:
                # print(product_data['title'])
                
                image_url = product_data['main_picture']
                if image_url:
                    response = requests.get(image_url , stream=True)
                    if response.status_code == 200:
                        # Create a temporary file to save the image
                        temp_image = os.path.join(current_directory, 'temp_image.jpg')
                        with open(temp_image , 'wb') as temp_file:
                            for chunk in response.iter_content(1024):
                                temp_file.write(chunk)
                else:
                    self.stdout.write(self.style.ERROR('Failed to download image.'))
                    
                brand , created = Brand.objects.get_or_create(brand_name = product_data['brand'])
                product, created = Product.objects.get_or_create(
                    title=product_data['title'],
                    SKU_number=product_data['SKU_number'],
                    selling_price=int(product_data['selling_price'].replace(',', '')),
                    discounted_price=int(product_data['discounted_price'].replace(',', '')),
                    original_selling_price = int(product_data['original_selling_price'].replace(',' , '')),
                    quantity=product_data['qunatity'],
                    main_picture=File(open(temp_image, 'rb')),
                    category = Category.objects.get(name__iexact = product_data['category']),
                    available_stock = product_data['available_stock'],
                    short_description = product_data['short_description'],
                    long_description = product_data['long_description'],
                    brand = brand,
                    url = product_data['url'],
                    # Add other fields as needed
                )
                # Remove the temporary main product image
                if os.path.exists(temp_image):
                    os.remove(temp_image)
                # Handle Product Images
                allimage_url = product_data.get('RelatedImages', [])
                if len(allimage_url) > 1:
                    allimage_url = allimage_url[1:]
                    for img_url in allimage_url:
                        response = requests.get(img_url, stream=True, allow_redirects=True)
                        if response.status_code == 200:
                            temp_allimg = os.path.join(current_directory, 'temp_allimg.jpg')
                            with open(temp_allimg, 'wb') as temp_img:
                                temp_img.write(response.content)
                                product_img = Product_images.objects.create(
                                    product= product ,
                                    RelatedImages=File(open(temp_allimg, 'rb'))
                                )
                                # product_images.append(product_img)
                        else:
                            self.stdout.write(self.style.ERROR(f'Failed to download image from URL: {img_url}'))
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Product "{product.title}" created successfully.'))
                else:
                    self.stdout.write(self.style.SUCCESS(f'Product "{product.title}" already exists.'))
                    
