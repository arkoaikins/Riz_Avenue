from store.models import Product, CartOrder, CartOrderProduct, Brand
from store.serializer import (
    ProductSerializer,
    PictureSerializer,
    SpecificationSerializer,
    ColorSerializer,
    SizeSerializer,
    BrandStatsSerializer,
)
from brand.models import Brand
from django.db import models, transaction
from django.db.models.functions import ExtractMonth

from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class BrandStatsView(generics.ListAPIView):
    """
    Retrieve statistics for a brand.

    This endpoint returns the summary statistics including the number of
    products,orders, and total income for a specific brand.
    """

    serializer_class = BrandStatsSerializer
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        operation_summary="Retrieve Brand Statistics",
        operation_description="Retrieve summary statistics including the"
        "number of products, orders, and total income for a specific brand"
        "data type Int",
        responses={
            200: openapi.Response(
                description="OK - Returns summary statistics for the"
                "specified brand."
            ),
            404: openapi.Response(description="Not Found - Brand not found."),
            500: openapi.Response(
                description="Server Error - Internal server error."),
        },
    )
    def get_queryset(self):
        """
        Method to retrieve summary statistics for a brand.
        """
        brand_id = self.kwargs["brand_id"]
        brand = Brand.objects.get(id=brand_id)

        # Calculate summary
        product_count = Product.objects.filter(brand=brand).count()
        order_count = CartOrder.objects.filter(
            brand=brand, payment_status="paid"
        ).count()
        income = (
            CartOrderProduct.objects.filter(
                brand=brand, order__payment_status="paid"
            ).aggregate(
                total_income=models.Sum(
                    models.F("sub_total") + models.F("shipping_amount")
                )
            )[
                "total_income"
            ]
            or 0
        )

        # Return list
        return [
            {
                "products": product_count,
                "orders": order_count,
                "income": income
                }
            ]

    @swagger_auto_schema(
        operation_summary="List Brand Statistics",
        operation_description="Retrieve summary statistics including the"
        "number of products, orders, and total income for a specific brand"
        "data type Int.",
        responses={
            200: openapi.Response(
                description="OK - Returns summary statistics for the"
                "specified brand."
            ),
            404: openapi.Response(description="Not Found - Brand not found."),
            500: openapi.Response(
                description="Server Error - Internal server error."),
        },
    )
    def list(self, request, *args, **kwargs):
        """
        Method to list summary statistics for a brand.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


@swagger_auto_schema(
    methods=["GET"],
    operation_summary="Get Monthly Orders for a Brand",
    operation_description="Retrieve monthly order statistics"
    "for a specific brand.",
    responses={
        200: openapi.Response(
            description="OK - Returns monthly order statistics"
            "for the specified brand."
        ),
        404: openapi.Response(description="Not Found - Brand not found."),
        500: openapi.Response(description="Server Error - Internal"
                              "server error."),
    },
)
@api_view(("GET",))
def MonthlyOrders(request, brand_id):
    """
    Get the Monthly Orders from this brand-- Chart(stats)
    """
    brand = Brand.objects.get(id=brand_id)
    orders = CartOrder.objects.filter(brand=brand, payment_status="paid")
    orders_month = (
        orders.annotate(month=ExtractMonth("date"))
        .values("month")
        .annotate(orders=models.Count("id"))
        .order_by("month")
    )
    return Response(orders_month)


@swagger_auto_schema(
    methods=["GET"],
    operation_summary="Get Monthly Added Products for a Brand",
    operation_description="Retrieve monthly added product statistics"
    "for a specific brand.",
    responses={
        200: openapi.Response(
            description="OK - Returns monthly added product statistics"
            "for the specified brand."
        ),
        404: openapi.Response(description="Not Found - Brand not found."),
        500: openapi.Response(
            description="Server Error - Internal server error."),
    },
)
@api_view(("GET",))
def MonthlyAddedProducts(request, brand_id):
    """
    Get Monthly Added Products for a Brand
    """
    brand = Brand.objects.get(id=brand_id)
    products = Product.objects.filter(brand=brand)
    products_month = (
        products.annotate(month=ExtractMonth("date"))
        .values("month")
        .annotate(products=models.Count("id"))
        .order_by("month")
    )
    return Response(products_month)


class ProductCreateView(generics.CreateAPIView):
    """
    View for creating a new product
    """

    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    @transaction.atomic
    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        serializer.save()
        product_instance = serializer.instance

        specifications_data = []
        colors_data = []
        sizes_data = []
        picture_data = []
        # Loop through the keys of self.request.data
        for key, value in self.request.data.items():
            # Example key: specifications[0][title]
            if key.startswith("specifications") and "[title]" in key:
                # Extract index from key
                index = key.split("[")[1].split("]")[0]
                title = value
                content_key = f"specifications[{index}][content]"
                content = self.request.data.get(content_key)
                specifications_data.append(
                    {"title": title, "content": content})

            # Example key: colors[0][name]
            elif key.startswith("colors") and "[name]" in key:
                # Extract index from key
                index = key.split("[")[1].split("]")[0]
                name = value
                color_code_key = f"colors[{index}][color_code]"
                color_code = self.request.data.get(color_code_key)
                colors_data.append({"name": name, "color_code": color_code})

            # Example key: sizes[0][name]
            elif key.startswith("sizes") and "[name]" in key:
                # Extract index from key
                index = key.split("[")[1].split("]")[0]
                name = value
                price_key = f"sizes[{index}][price]"
                price = self.request.data.get(price_key)
                sizes_data.append({"name": name, "price": price})

            # Example key: gallery[0][image]
            elif key.startswith("gallery") and "[image]" in key:
                # Extract index from key
                index = key.split("[")[1].split("]")[0]
                image = value
                picture_data.append({"image": image})

        # Log or print the data for debugging
        print("specifications_data:", specifications_data)
        print("colors_data:", colors_data)
        print("sizes_data:", sizes_data)
        print("picture_data:", picture_data)

        # Save nested serializers with the product instance
        self.save_nested_data(
            product_instance, SpecificationSerializer, specifications_data
        )
        self.save_nested_data(product_instance, ColorSerializer, colors_data)
        self.save_nested_data(product_instance, SizeSerializer, sizes_data)
        self.save_nested_data(
            product_instance, PictureSerializer, picture_data)

    @swagger_auto_schema(
        operation_summary="Create Product with Required Fields",
        operation_description="Create a new product with the required"
        "fields: title, brand, and slug.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "title": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Product title"
                ),
                "brand": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="Brand ID"
                ),
                "slug": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Product slug"
                ),
                "description": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Product description",
                    default="",
                ),
                "category": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="Category ID", default=1
                ),
                "price": openapi.Schema(
                    type=openapi.TYPE_NUMBER,
                    description="Product price", default=0.0
                ),
                "old_price": openapi.Schema(
                    type=openapi.TYPE_NUMBER,
                    description="Product old price",
                    default=0.0,
                ),
                "shipping_amount": openapi.Schema(
                    type=openapi.TYPE_NUMBER,
                    description="Shipping amount", default=0.0
                ),
                "stock_qty": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="Stock quantity", default=0
                ),
                "in_stock": openapi.Schema(
                    type=openapi.TYPE_BOOLEAN,
                    description="Is the product in stock",
                    default=True,
                ),
                "status": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Product status",
                    default="draft",
                ),
                "featured": openapi.Schema(
                    type=openapi.TYPE_BOOLEAN,
                    description="Is the product featured",
                    default=False,
                ),
                "views": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="Number of product views",
                    default=0,
                ),
                "rating": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="Product rating"
                ),
                "pid": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Product ID"
                ),
                "date": openapi.Schema(
                    type=openapi.FORMAT_DATETIME,
                    description="Date of creation",
                    default="2024-04-01T21:33:08.555Z",
                ),
            },
            required=["title", "brand", "slug"],
        ),
        responses={
            201: openapi.Response(
                description="Created - Product created successfully"),
            400: openapi.Response(
                description="Bad Request - If the request data is invalid"
            ),
            500: openapi.Response(
                description="Server Error - Internal server error"),
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def save_nested_data(self, product_instance, serializer_class, data):
        """
        Save product
        """
        serializer = serializer_class(
            data=data, many=True,
            context={"product_instance": product_instance}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(product=product_instance)


class ProductUpdateView(generics.RetrieveUpdateAPIView):
    """
    Update Prduct view

    Update product details api view
    """

    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def get_object(self):
        brand_id = self.kwargs["brand_id"]
        product_pid = self.kwargs["product_pid"]

        brand = Brand.objects.get(id=brand_id)
        product = Product.objects.get(pid=product_pid, brand=brand)
        return product

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        product = self.get_object()

        # Deserialize product data
        serializer = self.get_serializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Delete all existing nested data
        product.specification().delete()
        product.color().delete()
        product.size().delete()
        product.picture().delete()

        specifications_data = []
        colors_data = []
        sizes_data = []
        picture_data = []
        # Loop through the keys of self.request.data
        for key, value in self.request.data.items():
            # Example key: specifications[0][title]
            if key.startswith("specifications") and "[title]" in key:
                # Extract index from key
                index = key.split("[")[1].split("]")[0]
                title = value
                content_key = f"specifications[{index}][content]"
                content = self.request.data.get(content_key)
                specifications_data.append(
                    {"title": title, "content": content})

            # Example key: colors[0][name]
            elif key.startswith("colors") and "[name]" in key:
                # Extract index from key
                index = key.split("[")[1].split("]")[0]
                name = value
                color_code_key = f"colors[{index}][color_code]"
                color_code = self.request.data.get(color_code_key)
                colors_data.append({"name": name, "color_code": color_code})

            # Example key: sizes[0][name]
            elif key.startswith("sizes") and "[name]" in key:
                # Extract index from key
                index = key.split("[")[1].split("]")[0]
                name = value
                price_key = f"sizes[{index}][price]"
                price = self.request.data.get(price_key)
                sizes_data.append({"name": name, "price": price})

            # Example key: gallery[0][image]
            elif key.startswith("gallery") and "[image]" in key:
                # Extract index from key
                index = key.split("[")[1].split("]")[0]
                image = value
                picture_data.append({"image": image})

        # Log or print the data for debugging
        print("specifications_data:", specifications_data)
        print("colors_data:", colors_data)
        print("sizes_data:", sizes_data)
        print("picture_data:", picture_data)

        # Save nested serializers with the product instance
        self.save_nested_data(
            product, SpecificationSerializer, specifications_data)
        self.save_nested_data(product, ColorSerializer, colors_data)
        self.save_nested_data(product, SizeSerializer, sizes_data)
        self.save_nested_data(product, PictureSerializer, picture_data)

    def save_nested_data(self, product_instance, serializer_class, data):
        """
        Save updated product
        """
        serializer = serializer_class(
            data=data,
            many=True,
            context={"product_instance": product_instance}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(product=product_instance)


class ProductDeleteView(generics.DestroyAPIView):
    """
    Delete product

    Delete product from a brand
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)

    def get_object(self, *args, **kwargs):
        """ """
        brand_id = self.kwargs["brand_id"]
        product_pid = self.kwargs["product_pid"]

        brand = Brand.objects.get(id=brand_id)
        product = Product.objects.get(brand=brand, pid=product_pid)
        return product

    def perform_destroy(self, instance):
        """ """
        instance.delete()
        return Response(
            {"message": "Product deleted successfully"},
            status=status.HTTP_200_OK
        )
