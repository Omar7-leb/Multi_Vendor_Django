# from PIL import Image
# from django.http import HttpResponse
# from django.shortcuts import render
#
# # Create your views here.
# # Import the libraries
# from tensorflow.keras.preprocessing import image
# from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
# from tensorflow.keras.models import Model
# from pathlib import Path
# import numpy as np
#
#
# def ProcessDB(request):
#     for img_path in sorted("<IMAGE DATABASE PATH LIST HERE>"):
#         # Extract Features
#         fe = FeatureExtractor()
#         feature = fe.extract(img=Image.open(img_path))
#         # Save the Numpy array (.npy) on designated path
#         feature_path = "print(img_path)<IMAGE FEATURE PATH HERE>.npy"
#         np.save(feature_path, feature)
#
#     return HttpResponse("DB Processed!")
#
#
# class FeatureExtractor:
#
#     def __init__(self):
#         # Use VGG-16 as the architecture and ImageNet for the weight
#         base_model = VGG16(weights='imagenet')
#         # Customize the model to return features from fully-connected layer
#         self.model = Model(inputs=base_model.input, outputs=base_model.get_layer('fc1').output)
#
#     def extract(self, img):
#         # Resize the image
#         img = img.resize((224, 224))
#         # Convert the image color space
#         img = img.convert('RGB')
#         # Reformat the image
#         x = image.img_to_array(img)
#         x = np.expand_dims(x, axis=0)
#         x = preprocess_input(x)
#         # Extract Features
#         feature = self.model.predict(x)[0]
#         return feature / np.linalg.norm(
#             feature)  # Iterate through images (Change the path based on your image location)
