from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import RegisterSerializer
from rest_framework.response import Response

# Create your views here.


class RegisterAPIView(APIView):
   
    def post(self,request):
        serializer = RegisterSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"User" :"Created"})
        return Response(serializer.errors)







class LoginAPIView(APIView):
    pass