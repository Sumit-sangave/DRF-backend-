from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.response import Response
from django.core.mail import send_mail
import random
from .models import CustomUser, OTP
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions

# User Registration View
class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()

    def create(self, request, *args, **kwargs):
        # Extract user data from request
        user_data = request.data

        # Create the user instance
        user = CustomUser(
            username=user_data.get('username'),
            email=user_data.get('email'),
            first_name=user_data.get('first_name'),
            last_name=user_data.get('last_name'),
            middle_name=user_data.get('middle_name'),
            date_of_birth=user_data.get('date_of_birth'),
            gender=user_data.get('gender'),
            contact_number=user_data.get('contact_number'),
            hobbies=user_data.get('hobbies'),
            address=user_data.get('address'),
            language=user_data.get('language'),
        )
        user.set_password(user_data.get('password'))  # Hash the password
        user.save()  # Save the user instance

        # Generate and send OTP
        otp_code = random.randint(100000, 999999)
        OTP.objects.create(user=user, otp_code=otp_code)
        send_mail(
            'Your OTP Code',
            f'Your OTP code is {otp_code}',
            'sumitsangave2631@gmail.com',  # Replace with your actual email
            [user.email],
            fail_silently=False,
        )

        # Return the user ID and a success message
        return Response({
            'id': user.id,  # User ID
            'message': 'User registered successfully. OTP sent to email.'
        }, status=status.HTTP_201_CREATED)


# OTP Verification View
class VerifyOTPView(APIView):
    def post(self, request, *args, **kwargs):
        otp_code = request.data.get('otp_code')
        user_id = request.data.get('user_id')

        try:
            otp = OTP.objects.get(user_id=user_id, otp_code=otp_code)
            if not otp.is_verified:
                otp.is_verified = True
                otp.save()
                return Response({"message": "OTP verified successfully."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "OTP is already verified."}, status=status.HTTP_400_BAD_REQUEST)
        except OTP.DoesNotExist:
            return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)


# User Login View
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken

logger = logging.getLogger(__name__)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        logger.debug(f"Attempting to log in with username: {username}")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)

                refresh = RefreshToken.for_user(user)
                access = str(refresh.access_token)

                logger.info(f"Login successful for user: {username}")

                return Response({
                    'message': 'Login successful!',
                    'refresh': str(refresh),
                    'access': access,
                }, status=status.HTTP_200_OK)
            else:
                logger.warning(f"User {username} is inactive.")
                return Response({'error': 'User is inactive.'}, status=status.HTTP_403_FORBIDDEN)
        else:
            logger.warning(f"Authentication failed for user: {username}")
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


# Profile View for user profiles
# class Profile(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request):
#         users = CustomUser.objects.all().values()  # Retrieve all user profiles
#         return Response(users, status=status.HTTP_200_OK)

#     def post(self, request):
#         user_id = request.data.get('user_id')  # Get user ID from request data
#         try:
#             user = CustomUser.objects.get(id=user_id)  # Fetch the user profile
#             user_data = {
#                 'id': user.id,
#                 'username': user.username,
#                 'email': user.email,
#                 'first_name': user.first_name,
#                 'last_name': user.last_name,
#                 'middle_name': user.middle_name,
#                 'date_of_birth': user.date_of_birth,
#                 'gender': user.gender,
#                 'contact_number': user.contact_number,
#                 'hobbies': user.hobbies,
#                 'address': user.address,
#                 'language': user.language,
#             }
#             return Response(user_data, status=status.HTTP_200_OK)
#         except CustomUser.DoesNotExist:
#             return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

#     def put(self, request):
#         user_id = request.data.get('user_id')  # Get user ID from request data
#         try:
#             user = CustomUser.objects.get(id=user_id)  # Fetch the user profile
#             user.username = request.data.get('username', user.username)
#             user.email = request.data.get('email', user.email)
#             user.first_name = request.data.get('first_name', user.first_name)
#             user.last_name = request.data.get('last_name', user.last_name)
#             user.middle_name = request.data.get('middle_name', user.middle_name)
#             user.date_of_birth = request.data.get('date_of_birth', user.date_of_birth)
#             user.gender = request.data.get('gender', user.gender)
#             user.contact_number = request.data.get('contact_number', user.contact_number)
#             user.hobbies = request.data.get('hobbies', user.hobbies)
#             user.address = request.data.get('address', user.address)
#             user.language = request.data.get('language', user.language)

#             user.save()  # Save the updated user instance

#             return Response({'message': 'User profile updated successfully.'}, status=status.HTTP_200_OK)
#         except CustomUser.DoesNotExist:
#             return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)


# User Logout View
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logout(request)
        return JsonResponse({'message': 'Logout successful'}, status=status.HTTP_200_OK)


# Home/Dashboard View (Django template-based)
@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')

@login_required
def Main(request):
    return render(request, 'main.html')

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import CustomUser




# User Profile View (Django template-based)
@login_required
def profile_view(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})


# User Settings View (Django template-based)
@login_required
def settings_view(request):
    return render(request, 'settings.html', {'user': request.user})




# Get user profile
@login_required
def user_profile(request):
    if request.method == 'GET':
        user = request.user
        user_data = {
            "name": user.username,
            "email": user.email,
            "is_superuser": user.is_superuser
        }
        return JsonResponse(user_data)



from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.middleware.csrf import get_token
from django.contrib.auth.models import User
import json

@login_required
@require_http_methods(["GET", "POST"])
def profile_view(request):
    user = request.user
    if request.method == "GET":
        # Fetch user profile data
        profile_data = {
            "name": user.get_full_name(),
            "email": user.email,
            "is_superuser": user.is_superuser,
        }
        return JsonResponse(profile_data, status=200)

    elif request.method == "POST":
        # Update user profile data
        try:
            data = json.loads(request.body)
            user.first_name = data.get("first_name", user.first_name)
            user.last_name = data.get("last_name", user.last_name)
            user.email = data.get("email", user.email)
            user.save()
            return JsonResponse({"message": "Profile updated successfully"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        
        
        
# views.py
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Ensure that the user is authenticated
def check_superuser(request):
    """
    Check if the authenticated user is a superuser.
    """
    return Response({"is_superuser": request.user.is_superuser})

# views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Product
from rest_framework.response import Response

class ProductViewSet(viewsets.ViewSet):
    """
    A viewset for viewing products.
    """
    permission_classes = [IsAuthenticated]

    def list(self, request):
        # Fetch all products
        products = Product.objects.all()
        product_data = [
            {
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'price': product.price,
                'image': product.image.url if product.image else None
            }
            for product in products
        ]
        return Response(product_data)


# views.py
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.core.files.storage import default_storage
from django.conf import settings
from .models import Product

class AddProductView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Check if the user is a superuser
        if not request.user.is_superuser:
            return JsonResponse({'error': 'Only superusers can add products.'}, status=403)

        # Extract product data
        product_name = request.data.get('name')
        description = request.data.get('description')
        price = request.data.get('price')
        image = request.FILES.get('image')

        # Validate input
        if not product_name or not description or not price:
            return JsonResponse({'error': 'Missing required fields.'}, status=400)

        # Validate price
        try:
            price = float(price)
            if price <= 0:
                return JsonResponse({'error': 'Price must be a positive number.'}, status=400)
        except ValueError:
            return JsonResponse({'error': 'Invalid price format.'}, status=400)

        # Handle the image file
        image_path = None
        if image:
            try:
                image_path = f"products/{image.name}"
                default_storage.save(image_path, image)
            except Exception as e:
                return JsonResponse({'error': f'Error saving image: {str(e)}'}, status=500)

        # Create the product
        product = Product.objects.create(
            name=product_name,
            description=description,
            price=price,
            image=image_path
        )

        # Build the image URL
        image_url = request.build_absolute_uri(f'{settings.MEDIA_URL}{product.image}') if product.image else None

        return JsonResponse({
            'message': 'Product added successfully!',
            'product': {
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'price': product.price,
                'image': image_url
            }
        }, status=201)



# views.py
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Product

class GetProductsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Fetch all products
        products = Product.objects.all()
        product_list = [
            {
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'price': product.price,
                'image': request.build_absolute_uri(f'{settings.MEDIA_URL}{product.image}') if product.image else None
            }
            for product in products
        ]

        return JsonResponse(product_list, safe=False, status=200)



        
        

# # views.py
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.contrib.auth.decorators import login_required, user_passes_test
# from django.core.exceptions import PermissionDenied
# from .models import Product
# from django.shortcuts import get_object_or_404
# import json

# # View to list all products (accessible to all authenticated users)
# @login_required
# def get_products(request):
#     products = Product.objects.all()
#     products_data = [
#         {
#             "id": product.id,
#             "name": product.name,
#             "description": product.description,
#             "price": product.price,
#             "image": product.image.url if product.image else None,
#         }
#         for product in products
#     ]
#     return JsonResponse(products_data, safe=False)

# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.contrib.auth.decorators import user_passes_test
# from .models import Product

# @csrf_exempt
# @user_passes_test(lambda u: u.is_superuser)  # Ensure only superusers can upload products
# def upload_product(request):
#     if request.method == 'POST':  # Only allow POST method
#         try:
#             # Ensure the required fields are available
#             name = request.POST.get('name')
#             description = request.POST.get('description')
#             price = request.POST.get('price')
#             image = request.FILES.get('image')

#             # Check if the name and price are provided
#             if not name or not price:
#                 return JsonResponse({"error": "Name and price are required"}, status=400)

#             # Create a new product instance and save it
#             product = Product(
#                 name=name,
#                 description=description,
#                 price=price,
#                 image=image if image else None  # Use image if available, otherwise set as None
#             )
#             product.save()

#             # Return a success message with product details
#             return JsonResponse({
#                 "message": "Product uploaded successfully",
#                 "product_id": product.id,
#                 "name": product.name,
#                 "description": product.description,
#                 "price": product.price,
#                 "image": product.image.url if product.image else None  # If image is saved, provide its URL
#             })

#         except Exception as e:
#             # In case of any error, return the error message
#             return JsonResponse({"error": str(e)}, status=500)

#     # If method is not POST, return an error
#     return JsonResponse({"error": "Invalid method, POST only allowed"}, status=405)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Product, Cart

# Delete Product
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_product(request, product_id):
    if not request.user.is_superuser:
        return Response({"error": "Permission denied"}, status=403)
    
    # Fetch the product and delete
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return Response({"message": "Product deleted successfully"})

# Add to Cart
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    product_id = request.data.get('product_id')
    product = get_object_or_404(Product, id=product_id)
    
    # Ensure the product is not already in the user's cart
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if created:
        return Response({"message": "Product added to cart"})
    return Response({"message": "Product is already in your cart"})


# Get Cart Items
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    cart_data = [{"product_name": item.product.name, "price": item.product.price, "id": item.product.id} for item in cart_items]
    return Response(cart_data)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import CartItem

class RemoveFromCart(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        # Get the cart item by its ID (primary key)
        try:
            cart_item = CartItem.objects.get(pk=pk, user=request.user)
        except CartItem.DoesNotExist:
            return Response({'detail': 'Item not found in your cart'}, status=status.HTTP_404_NOT_FOUND)

        # Delete the cart item
        cart_item.delete()

        return Response({'detail': 'Item removed from cart'}, status=status.HTTP_204_NO_CONTENT)

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Product, Like, Comment
from django.db.models import Count
import json

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_likes(request):
    likes = Like.objects.values('product_id').annotate(like_count=Count('id'))
    like_dict = {like['product_id']: like['like_count'] for like in likes}
    return JsonResponse(like_dict)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def toggle_like(request):
    data = json.loads(request.body)
    product_id = data.get('product_id')
    user = request.user

    try:
        product = Product.objects.get(id=product_id)
        like, created = Like.objects.get_or_create(user=user, product=product)
        if not created:
            like.delete()
            liked = False
        else:
            liked = True

        like_count = Like.objects.filter(product=product).count()
        return JsonResponse({'liked': liked, 'likes_count': like_count})
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)
    
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def add_comment(request):
    data = json.loads(request.body)
    product_id = data.get('product_id')
    comment_text = data.get('comment')
    user = request.user

    try:
        product = Product.objects.get(id=product_id)
        Comment.objects.create(user=user, product=product, comment=comment_text)
        return JsonResponse({'message': 'Comment added successfully'})
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)