from django.urls import path 
from . import views
urlpatterns = [
    path('product/',views.ProductCreateList.as_view()),
    path('product/<int:pk>/',views.ProductRetriveUpdateDelete.as_view())
]
