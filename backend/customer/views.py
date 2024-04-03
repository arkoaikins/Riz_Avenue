from store.models import Product, CartOrder, Favorite
from store.serializer import CartOrderSerializer, FavouriteSerializer
from userauths.models import User

from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class OrdersView(generics.ListAPIView):
    """
    View for retrieving pending orders for a user
    """

    serializer_class = CartOrderSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        """
        Method to retrieve paid orders for a user.
        """
        try:
            user_id = self.kwargs["user_id"]
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise NotFound("User does not exist ")

        orders = CartOrder.objects.filter(buyer=user, payment_status="pending")
        return orders

    @swagger_auto_schema(
        operation_summary="Retrieve pending Orders for a User",
        operation_description="Retrieve a list of pending orders"
        "for a specific user.",
        responses={
            200: openapi.Response(
                description="OK - Returns a list of pending orders for"
                "the specified user."
            ),  # nopep8
            400: openapi.Response(
                description="Bad Request - If the provided user ID is invalid."
            ),  # nopep8
            404: openapi.Response(description="Not Found - User  not found."),  # nopep8
            500: openapi.Response(
                description="Server Error - Internal server error."
            ),  # nopep8
        },
    )
    def get(self, request, *args, **kwargs):
        """
        Retrieve user orders.
        """
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class OrdersDetailView(generics.RetrieveAPIView):
    """
    API endpoint for retrieving details of a specific order by a user.
    """

    serializer_class = CartOrderSerializer
    permission_classes = (AllowAny,)
    lookup_field = "user_id"

    def get_object(self):
        try:
            user_id = self.kwargs["user_id"]
            order_oid = self.kwargs["order_oid"]
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise NotFound("User does not exist ")
        order = CartOrder.objects.get(
            buyer=user, payment_status="pending", oid=order_oid
        )
        return order

    @swagger_auto_schema(
        operation_summary="Retrieve details of a specific order by a user",
        operation_description="Retrieve details of an order by a user using"
        "the order id.",
        responses={
            200: openapi.Response(
                description="OK - Returns details of order"
            ),  # nopep8
            400: openapi.Response(
                description="Bad Request - If the provided user ID is invalid."
            ),  # nopep8
            404: openapi.Response(description="Not Found - User  not found."),  # nopep8
            500: openapi.Response(
                description="Server Error - Internal server error."
            ),  # nopep8
        },
    )
    def get(self, request, *args, **kwargs):
        """
        Retrieve details of a specific order by a user.
        """
        instance = self.get_object()
        serializer = self.serializer_class(instance)
        return Response(serializer.data)


class FavouriteView(generics.ListCreateAPIView):
    """
    Add Products to fav

    pass in the product_id
    pass in the user_id
    and add the user_id down there

    When you run it it will add to fav
    When u run it again it will be removed from fav
    """

    serializer_class = FavouriteSerializer
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        operation_summary="Retrieve User Favorites",
        operation_description="Retrieve a list of favorite products for a"
        "specific user.",
        responses={
            200: openapi.Response(
                description="OK - Returns a list of favorite products for the"
                "specified user."
            ),
            404: openapi.Response(description="Not Found - User not found."),
            500: openapi.Response(description="Server Error - Internal server"
                                  "error."),
        },
    )
    def get(self, request, *args, **kwargs):
        """
        Retrieve a list of favorite products for a specific user.
        """
        user_id = self.kwargs["user_id"]
        user = User.objects.get(id=user_id)
        favorites = Favorite.objects.filter(user=user)
        serializer = self.serializer_class(favorites, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Add or Remove Product from Favorites",
        operation_description="Pass in the product_id and user_id to add or"
        "remove the product from favorites. When a product is added to"
        "favorites, running the endpoint again will remove it from favorites,"
        "and vice versa.",
        responses={
            200: openapi.Response(
                description="OK - Product removed from favorites."),
            201: openapi.Response(
                description="Created - Product added to favorites."),
        },
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "product": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="Product ID"
                ),
                "user": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="User ID"
                ),
            },
            required=["product", "user"],
        ),
    )
    def post(self, request, *args, **kwargs):
        """
        Add or remove a product from favorites.
        """
        payload = request.data

        product_id = payload["product"]
        user_id = payload["user"]

        product = Product.objects.get(id=product_id)
        user = User.objects.get(id=user_id)

        favorites = Favorite.objects.filter(product=product, user=user)
        if favorites:
            favorites.delete()
            return Response(
                {"message": "Product has been removed from favorites"},
                status=status.HTTP_200_OK,
            )
        else:
            Favorite.objects.create(product=product, user=user)
            return Response(
                {"message": "Product has been added to favorites"},
                status=status.HTTP_201_CREATED,
            )
