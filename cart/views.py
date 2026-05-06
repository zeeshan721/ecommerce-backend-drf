from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem
from product.models import Product  
from cart.models import Cart, CartItem
from .models import Order, OrderItem




class AddToCartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        # get product
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=404)

        # get or create cart
        cart, created = Cart.objects.get_or_create(user=user)

        # check if item exists
        cart_item, item_created = CartItem.objects.get_or_create(
            cart=cart,
            product=product
        )

        if not item_created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity

        cart_item.save()

        return Response({"message": "Product added to cart"})
    




class RemoveFromCartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        product_id = request.data.get('product_id')

        try:
            cart = Cart.objects.get(user=user)
            item = CartItem.objects.get(cart=cart, product_id=product_id)
            item.delete()

            return Response({"message": "Item removed from cart"})
        except:
            return Response({"error": "Item not found"}, status=404)
        




class UpdateCartQuantityAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity'))

        try:
            cart = Cart.objects.get(user=user)
            item = CartItem.objects.get(cart=cart, product_id=product_id)

            if quantity <= 0:
                item.delete()
                return Response({"message": "Item removed"})

            item.quantity = quantity
            item.save()

            return Response({"message": "Quantity updated"})
        except:
            return Response({"error": "Item not found"}, status=404)
        




class ViewCartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        try:
            cart = Cart.objects.get(user=user)
            items = CartItem.objects.filter(cart=cart)

            cart_data = []
            grand_total = 0

            for item in items:
                total = item.product.price * item.quantity
                grand_total += total

                cart_data.append({
                    "product": item.product.name,
                    "price": float(item.product.price),
                    "quantity": item.quantity,
                    "total": float(total)
                })

            return Response({
                "items": cart_data,
                "grand_total": float(grand_total)
            })

        except Cart.DoesNotExist:
            return Response({
                "items": [],
                "grand_total": 0
            })





class CheckoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        try:
            cart = Cart.objects.get(user=user)
            items = CartItem.objects.filter(cart=cart)

            if not items.exists():
                return Response({"error": "Cart is empty"}, status=400)

            total = 0

            # 1. CREATE ORDER (IMPORTANT FIX)
            order = Order.objects.create(
                user=user,
                total_price=0
            )

            # 2. CREATE ORDER ITEMS
            for item in items:
                total += item.product.price * item.quantity

                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    price=item.product.price,
                    quantity=item.quantity
                )

            # 3. UPDATE TOTAL
            order.total_price = total
            order.save()

            # 4. CLEAR CART
            items.delete()

            return Response({
                "message": "Order placed successfully",
                "order_id": order.id,
                "total": float(total)
            })

        except Cart.DoesNotExist:
            return Response({"error": "Cart not found"}, status=404)







class OrderHistoryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        orders = Order.objects.filter(user=user).order_by('-created_at')

        data = []

        for order in orders:
            items = order.items.all()

            item_list = []
            for item in items:
                item_list.append({
                    "product": item.product.name,
                    "price": float(item.price),
                    "quantity": item.quantity
                })

            data.append({
                "order_id": order.id,
                "status": order.status,
                "total_price": float(order.total_price),
                "created_at": order.created_at,
                "items": item_list
            })

        return Response(data)
    









#Order status 
class UpdateOrderStatusAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        new_status = request.data.get('status')

        if not new_status:
            return Response({"error": "status is required"}, status=400)

        try:
            order = Order.objects.get(id=order_id, user=request.user)

            order.status = new_status
            order.save()

            return Response({"message": "Order status updated"})

        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=404)