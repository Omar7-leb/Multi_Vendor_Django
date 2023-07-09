from PIL import Image
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
# Import the libraries
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.models import Model
from pathlib import Path
import numpy as np
from product.models import Product


def ProcessDB(request):
    products = Product.objects.all()
    features_list = []
    feature = []
    # Iterate over each product
    for p in products:
        # Extract Features
        print(p)
        fe = FeatureExtractor()
        feature = fe.extract(img=Image.open(p.image))
        print(feature)

        # Create a dictionary to store the ID and feature
        feature_dict = {'id': p.id, 'features': feature}
        features_list.append(feature_dict)

    # Convert the list of dictionaries to a structured NumPy array
    dtype = [('id', int), ('features', float, feature.shape)]
    features_with_id = np.zeros(len(features_list), dtype=dtype)
    for i, feature_dict in enumerate(features_list):
        features_with_id['id'][i] = feature_dict['id']
        features_with_id['features'][i] = feature_dict['features']

    # Save the NumPy array (.npy) to the designated path
    feature_path = "features.npy"
    np.save(feature_path, features_with_id)

    return HttpResponse("DB Processed!")


class FeatureExtractor:

    def __init__(self):
        # Use VGG-16 as the architecture and ImageNet for the weight
        base_model = VGG16(weights='imagenet')
        # Customize the model to return features from fully-connected layer
        self.model = Model(inputs=base_model.input, outputs=base_model.get_layer('fc1').output)

    def extract(self, img):
        # Resize the image
        img = img.resize((224, 224))
        # Convert the image color space
        img = img.convert('RGB')
        # Reformat the image
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        # Extract Features
        feature = self.model.predict(x)[0]
        return feature / np.linalg.norm(
            feature)  # Iterate through images (Change the path based on your image location)


def searchImage(request):
    if request.method == 'POST' and request.FILES['image']:
        image = request.FILES['image']
        # Save the image to a specific directory
        save_path = 'imageSearch/'
        with open(save_path + image.name, 'wb') as file:
            for chunk in image.chunks():
                file.write(chunk)
        # Additional processing or redirection
        # Insert the image query
        img = Image.open(save_path + image.name)
        # Extract its features
        fe = FeatureExtractor()
        query = fe.extract(img)
        # Calculate the similarity (distance) between images
        features = np.load('features.npy')
        dists = np.linalg.norm(features["features"] - query, axis=1)  # Extract 30 images that have lowest distance
        ids = np.argsort(dists)[:1]

        products_id = features[ids[0]]["id"]
        product = Product.objects.filter(id=products_id)[0]
        return render(request, 'imageSearch/upload_image.html', {"product": product})
    return render(request, 'imageSearch/upload_image.html', {"product": []})
