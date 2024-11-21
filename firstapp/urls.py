from django.urls import path
from .views import (UserRegistrationView, VerifyOTPView, LoginView, LogoutView, dashboard_view, profile_view, settings_view,)

from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from . import views

# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from .views import upload_product , get_products
from .views import RemoveFromCart,ProductViewSet
from django.urls import path
from .views import AddProductView, GetProductsView


# Set up a router for product-related views
router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')


urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('verify_otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/',  LogoutView.as_view(), name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('profile/', profile_view, name='profile'),
    path('settings/', settings_view, name='settings'),
    path('check_superuser/', views.check_superuser, name='check_superuser'),
    # path('upload_product/', upload_product, name='upload_product'),
    path('product/', views.Product, name='product'),  # View for listing products
    # path('get_products/', get_products, name='get_products'),
    # path('firstapp/', include(router.urls)), # Products URL will be prefixed with 'firstapp/'

    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),

    path('view_cart/', views.view_cart, name='view_cart'),
    path('firstapp/', include(router.urls)),
    
    path('upload_product/', AddProductView.as_view(), name='upload_product'),
    path('get_products/', GetProductsView.as_view(), name='get_products'),

    # path('get_products/', views.get_products, name='get_products'),
    path('get_likes/', views.get_likes, name='get_likes'),
    path('toggle_like/', views.toggle_like, name='toggle_like'),
    path('add_comment/', views.add_comment, name='add_comment'),
    
        # URL for removing an item from the cart
    path('remove_from_cart/<int:pk>/', RemoveFromCart.as_view(), name='remove-from-cart'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




