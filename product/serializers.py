from rest_framework import serializers
from .models import Product
from rest_framework.pagination import PageNumberPagination



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields  = ['name','price','stock','media','status']



class MyPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 10