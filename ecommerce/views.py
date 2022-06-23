from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView
from ecommerce.custom_permissions import IsStaffOrReadOnly, IsOwnerOrReadOnly
from ecommerce.models import Category, Product
from ecommerce.serializers import CategorySerializer, ProductSerializer


# LINK PARA LA API
@api_view(["GET"])
def api_root_format(request, format=None):
    return Response(
        {
            "ecommerce": reverse("ecommerce:product-list", request=request, format=format),
            "category": reverse("ecommerce:category-list", request=request, format=format),
        }
    )


# AÑADIR SELLER, category no se está guardando al crear un prod
@api_view(["GET", "POST"])
def product_list(request):
    """
        Return a list of products by category
    """
    if request.method == "GET":
        queryset = Product.objects.select_related("category").all()
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = ProductSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return None


# @api_view(["GET", "PUT", "PATCH", "DELETE"])
# @user_is_seller
# def product_detail(request, slug):
#     product = get_object_or_404(Product, slug=slug)
#     if request.method == "GET":
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)
#     elif request.method in ("PUT", "PATCH"):
#         serializer = ProductSerializer(product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     elif request.method == "DELETE":
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#     return None


class ProductDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    lookup_field = 'slug'
    permission_classes = [IsOwnerOrReadOnly]

class CategoryList(ListAPIView, 
CreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsStaffOrReadOnly]


# @api_view(["GET", "POST"])
# def category_list(request):
#     if request.method == "GET":
#         queryset = Category.objects.all()
#         serializer = CategorySerializer(queryset, many=True)
#         return Response(serializer.data)
#     elif request.method == "POST":
#         serializer = CategorySerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return None


# Añadir regla para que regrese cuantos productos tiene cada categoriía y para que no deje eliminar cat si tiene algún prod
@api_view(["GET", "PUT", "PATCH", "DELETE"])
# @user_is_seller
def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    if request.method == "GET":
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    elif request.method in ("PUT", "PATCH"):
        serializer = CategorySerializer(category, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "DELETE":
        if category.products.count() > 0:
            return Response({"error": "La colección no se puede eliminar porque tiene productos"})
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return None
