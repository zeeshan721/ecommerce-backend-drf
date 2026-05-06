from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.AddToCartAPIView.as_view()),
    path('remove/',views.RemoveFromCartAPIView.as_view()),
    path('update/', views.UpdateCartQuantityAPIView.as_view()),
    path('view/', views.ViewCartAPIView.as_view()),
    path('checkout/', views.CheckoutAPIView.as_view()),
    path('orders/', views.OrderHistoryAPIView.as_view()),
    path('order/update/<int:order_id>/', views.UpdateOrderStatusAPIView.as_view()),
    
]
