from django.shortcuts import render
from django.http import HttpResponse
from .search import lookup

# Create your views here.

def getProducts(request):
    lookup(query="test")
    return HttpResponse("Hello world!")
