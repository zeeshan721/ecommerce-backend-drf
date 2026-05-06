from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ProductSerializer,MyPagination
from .models import Product
from .models import Product
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.generics import ListCreateAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
# Create your views here.





class ProductCreateList(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    pagination_class = MyPagination
    
    # permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['price', 'stock']
    search_fields = ['name']
    ordering_fields = ['price', 'id']




class ProductRetriveUpdateDelete(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer    





