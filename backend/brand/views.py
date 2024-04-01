from django.shortcuts import render

from store.models import Cart, Notification, Product, Category, CartOrder,CartOrderProduct, Picture, Brand, Review,  Specification, Coupon, Color, Size, Favorite, ProductFAQ, Tax
from store.serializer import  CartSerializer, CartOrderProductSerializer, ProductSerializer, CategorySerializer, CartOrderSerializer, PictureSerializer, BrandSerializer, ProductFAQSerializer, ReviewSerializer,  SpecificationSerializer, CouponSerializer, ColorSerializer, SizeSerializer, FavouriteSerializer,NotificationSerializer,BrandStatsSerializer
from userauths.models import User
from brand.models import Brand
from django.db import models, transaction
from django.db.models.functions import ExtractMonth

from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view
from decimal import Decimal

class BrandStatsView(generics.ListAPIView):
    """
    """
    serializer_class = BrandStatsSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        """
        """
        brand_id = self.kwargs['brand_id']
        brand = Brand.objects.get(id=brand_id)

        # Calculate summary 
        product_count = Product.objects.filter(brand=brand).count()
        order_count = CartOrder.objects.filter(brand=brand, payment_status="paid").count()
        income = CartOrderProduct.objects.filter(brand=brand, order__payment_status="paid").aggregate(
            total_income=models.Sum(models.F('sub_total') + models.F('shipping_amount')))['total_income'] or 0

        # Return list 
        return [{
            'products': product_count,
            'orders': order_count,
            'income': income
        }]

    def list(self, request, *args, **kwargs):
        """
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    
@api_view(('GET',))
def MonthlyOrders(request, brand_id):
    """
    Get the Monthly Orders from this brand-- Chart(stats)
    """
    brand = Brand.objects.get(id=brand_id)
    orders = CartOrder.objects.filter(brand=brand, payment_status="paid")
    orders_month = orders.annotate(month=ExtractMonth("date")).values(
        "month").annotate(orders=models.Count("id")).order_by("month")
    return Response(orders_month)


@api_view(('GET',))
def MonthlyAddedProducts(request, brand_id):
    """
    Get the Monthly Orders from this brand-- Chart(stats)
    """
    brand = Brand.objects.get(id=brand_id)
    products = Product.objects.filter(brand=brand)
    products_month = products.annotate(month=ExtractMonth("date")).values(
        "month").annotate(products=models.Count("id")).order_by("month")
    return Response(products_month)

