@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_product(request):
    product_id = request.data.get('product_id')
    product = get_object_or_404(Product, id=product_id)
    
    # Ensure the like is unique per user and product
    like, created = Like.objects.get_or_create(user=request.user, product=product)
    if created:
        return Response({"message": "Product liked"})
    return Response({"message": "Product already liked"})

# Comment on Product
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment_product(request):
    product_id = request.data.get('product_id')