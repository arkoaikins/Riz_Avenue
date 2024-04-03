from store.models import (
    Cart,
    Product,
    Category,
    CartOrder,
    CartOrderProduct,
    Review,
    ProductFAQ,
    Tax,
)
from store.serializer import (
    CartSerializer,
    ProductSerializer,
    CategorySerializer,
    CartOrderSerializer,
    ProductFAQSerializer,
    ReviewSerializer,
)
from userauths.models import User

from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from decimal import Decimal


class CategoryListView(generics.ListAPIView):
    """
    List all categories.
    """

    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        operation_summary="Retrieve a list of all categories",
        operation_description="List all the categories of products",
        responses={200: CategorySerializer(many=True)},
        tags=["Categories"],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ProductListView(generics.ListAPIView):
    """
    List all products.
    """

    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        operation_summary="Retrieve a list of all Products",
        operation_description="List all the products",
        responses={200: ProductSerializer(many=True)},
        tags=["Products"],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ProductDetailView(generics.RetrieveAPIView):
    """
    Gets the details of a product using the provided slug
    """

    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        operation_summary="Retrieve details of a product",
        operation_description="Retrieve the details of a product using its slug.",
        manual_parameters=[
            openapi.Parameter(
                "slug",
                openapi.IN_PATH,
                description="Product slug",
                type=openapi.TYPE_STRING,
            )
        ],
        responses={200: ProductSerializer()},
        tags=["Products"],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_object(self):
        """
        Overite the defualt get method and use slug
        """
        slug = self.kwargs.get("slug")
        return Product.objects.get(slug=slug)


class CartView(generics.ListCreateAPIView):
    """
    List all cart items or create a new cart item.
    """

    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        operation_summary="List all carts for all users(beta feature)",
        operation_description="List all cart items for all users",
        responses={
            200: CartSerializer(many=True),
            201: CartSerializer(),
            400: "Bad request",
        },
        tags=["Cart"],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        Create a new cart item
        Overite create method
        All items that are added to cart by the user
        will be stored in the payload

        to store Cart items in the payload

        """
        payload = request.data

        product_id = payload["product_id"]
        user_id = payload["user_id"]
        qty = payload["qty"]
        price = payload["price"]
        shipping_amount = payload["shipping_amount"]
        country = payload["country"]
        size = payload["size"]
        color = payload["color"]
        cart_id = payload["cart_id"]

        # After getting the actual id's of the product
        # We then get the actual object and store it in its variables
        product = Product.objects.get(id=product_id)
        if user_id != "undefined":  # if user has an account
            user = User.objects.get(id=user_id)
        else:
            user = None

        tax = Tax.objects.filter(country=country).first()
        if tax:
            tax_rate = tax.rate / 100

        else:
            tax_rate = 0

        # Update any old cart with latest data from the model,if no cart exist we create a new one
        cart = Cart.objects.filter(cart_id=cart_id, product=product).first()
        if cart:
            cart.product = product
            cart.user = user
            cart.qty = qty
            cart.price = price
            cart.sub_total = Decimal(price) * int(qty)
            cart.shipping_amount = Decimal(shipping_amount) * int(qty)
            cart.size = size
            cart.tax_fee = int(qty) * Decimal(tax_rate)
            cart.color = color
            cart.country = country
            cart.cart_id = cart_id

            service_fee_amount = 5 / 100  # in percentage
            cart.service_fee = Decimal(service_fee_amount) * cart.sub_total

            cart.total = (
                cart.sub_total + cart.shipping_amount + cart.service_fee + cart.tax_fee
            )
            cart.save()

            return Response(
                {"message": "Cart has been updated successfully"},
                status=status.HTTP_200_OK,
            )

        # if there is no old cart(cart does not exist)
        else:
            cart.product = product
            cart.user = user
            cart.qty = qty
            cart.price = price
            cart.sub_total = Decimal(price) * int(qty)
            cart.shipping_amount = Decimal(shipping_amount) * int(qty)
            cart.size = size
            cart.tax_fee = int(qty) * Decimal(tax_rate)
            cart.color = color
            cart.country = country
            cart.cart_id = cart_id

            service_fee_amount = 5 / 100  # in percentage
            cart.service_fee = Decimal(service_fee_amount) * cart.sub_total

            cart.total = (
                cart.sub_total + cart.shipping_amount + cart.service_fee + cart.tax_fee
            )
            cart.save()

            return Response(
                {"message": "Cart has been Created successfully"},
                status=status.HTTP_201_CREATED,
            )


class CartListView(generics.ListAPIView):
    """
    List cart items
    """

    serializer_class = CartSerializer
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        operation_summary="List cart of a user",
        operation_description="List  carts details from their Id or add"
        "a user_id  get the details of a specific cart for a user",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        cart_id = self.kwargs["cart_id"]
        user_id = self.kwargs.get(
            "user_id"
        )  # Use get() method to handle the case where user_id is not present

        if user_id is not None:
            user = User.objects.get(id=user_id)
            queryset = Cart.objects.filter(user=user, cart_id=cart_id)
        else:
            queryset = Cart.objects.filter(cart_id=cart_id)

        return queryset


class CartDetailView(generics.RetrieveAPIView):
    """
    Retrieve Payment calculations of a cart

    Retrieve the payment informations of a cart or of a cart of a particular user
    """

    serializer_class = CartSerializer
    permission_classes = (AllowAny,)
    lookup_field = "cart_id"

    def get_queryset(self):
        """
        Retrieve cart items by cart_id
        """
        # Get 'cart_id' and 'user_id' from the URL kwargs
        cart_id = self.kwargs["cart_id"]
        user_id = self.kwargs.get(
            "user_id"
        )  # Use get() method to handle the case where user_id is not present

        if user_id is not None:
            # If 'user_id' is provided, filter the queryset by both 'cart_id' and 'user_id'
            user = User.objects.get(id=user_id)
            queryset = Cart.objects.filter(user=user, cart_id=cart_id)
        else:
            # If 'user_id' is not provided, filter the queryset by 'cart_id' only
            queryset = Cart.objects.filter(cart_id=cart_id)

        return queryset

    def get(self, request, *args, **kwargs):
        # Get the queryset of cart items based on 'cart_id' and 'user_id' (if provided)
        queryset = self.get_queryset()

        # Initialize sums for various cart item attributes
        total_shipping = 0.0
        total_tax = 0.0
        total_service_fee = 0.0
        total_sub_total = 0.0
        total_total = 0.0

        # Iterate over the queryset of cart items to calculate cumulative sums
        for cart_item in queryset:
            # Calculate the cumulative shipping
            total_shipping += float(self.calculate_shipping(cart_item))
            total_tax += float(self.calculate_tax(cart_item))
            total_service_fee += float(self.calculate_service_fee(cart_item))
            total_sub_total += float(self.calculate_sub_total(cart_item))
            total_total += round(float(self.calculate_total(cart_item)), 2)

        # Create a data dictionary to store the cumulative value
        data = {
            "shipping": round(total_shipping, 2),
            "tax": total_tax,
            "service_fee": total_service_fee,
            "sub_total": total_sub_total,
            "total": total_total,
        }

        # Return the data in the response
        return Response(data)

    def calculate_shipping(self, cart_item):
        # Implement your shipping calculation logic here for a single cart item
        # Example: Calculate based on weight, destination, etc.
        return cart_item.shipping_amount

    def calculate_tax(self, cart_item):
        # Implement your tax calculation logic here for a single cart item
        # Example: Calculate based on tax rate, product type, etc.
        return cart_item.tax_fee

    def calculate_service_fee(self, cart_item):
        # Implement your service fee calculation logic here for a single cart item
        # Example: Calculate based on service type, cart total, etc.
        return cart_item.service_fee

    def calculate_sub_total(self, cart_item):
        # Implement your service fee calculation logic here for a single cart item
        # Example: Calculate based on service type, cart total, etc.
        return cart_item.sub_total

    def calculate_total(self, cart_item):
        # Implement your total calculation logic here for a single cart item
        # Example: Sum of sub_total, shipping, tax, and service_fee
        return cart_item.total


class CartItemDeleteView(generics.DestroyAPIView):
    """
    Delete an item in a cart

    Delete a product from a cart or a product from a cart of a particular user
    """

    serializer_class = CartSerializer
    lookup_field = "cart_id"

    def get_object(self):
        cart_id = self.kwargs["cart_id"]
        item_id = self.kwargs["item_id"]
        user_id = self.kwargs.get("user_id")

        if user_id:
            user = User.objects.get(id=user_id)
            cart = Cart.objects.get(id=item_id, cart_id=cart_id, user=user)
        else:
            cart = Cart.objects.get(id=item_id, cart_id=cart_id)

        return cart


class CreateOrderView(generics.CreateAPIView):
    """
    Create an order

    Initiating an order to be buy a product
    """

    serializer_class = CartOrderSerializer
    queryset = CartOrder.objects.all()
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        payload = request.data

        full_name = payload["full_name"]
        email = payload["email"]
        phone = payload["phone"]
        address = payload["address"]
        city = payload["city"]
        state = payload["state"]
        country = payload["country"]
        cart_id = payload["cart_id"]
        user_id = payload["user_id"]

        # print("user_id ===============", user_id)

        if user_id != 0:
            user = User.objects.filter(id=user_id).first()
        else:
            user = None
        # grab all items in the cart
        cart_items = Cart.objects.filter(cart_id=cart_id)

        total_shipping = Decimal(0.00)
        total_tax = Decimal(0.00)
        total_service_fee = Decimal(0.00)
        total_sub_total = Decimal(0.00)
        total_initial_total = Decimal(0.00)
        total_total = Decimal(0.00)

        order = CartOrder.objects.create(
            buyer=user,
            full_name=full_name,
            email=email,
            phone=phone,
            address=address,
            city=city,
            state=state,
            country=country,
        )

        for c in cart_items:
            CartOrderProduct.objects.create(
                order=order,
                product=c.product,
                brand=c.product.brand,
                qty=c.qty,
                color=c.color,
                size=c.size,
                price=c.price,
                sub_total=c.sub_total,
                shipping_amount=c.shipping_amount,
                service_fee=c.service_fee,
                tax_fee=c.tax_fee,
                total=c.total,
                initial_total=c.total,
            )
            total_shipping += Decimal(c.shipping_amount)
            total_tax += Decimal(c.tax_fee)
            total_service_fee += Decimal(c.service_fee)
            total_sub_total += Decimal(c.sub_total)
            total_initial_total += Decimal(c.total)
            total_total += Decimal(c.total)

            order.brand.add(c.product.brand)

        order.sub_total = total_sub_total
        order.shipping_amount = total_shipping
        order.tax_fee = total_tax
        order.service_fee = total_service_fee
        order.initial_total = total_initial_total
        order.total = total_total

        order.save()

        return Response(
            {"message": "Order has been Created Successfully", "order_oid": order.oid},
            status=status.HTTP_201_CREATED,
        )


class CheckoutView(generics.RetrieveAPIView):
    """
    Retrieve checkout details.


    Use the order_id to check the details of the order you have made
    """

    serializer_class = CartOrderSerializer
    lookup_field = "order_oid"

    def get_object(self):
        """
        Retrieve checkout details by order_oid.
        """
        order_oid = self.kwargs["order_oid"]
        order = CartOrder.objects.get(oid=order_oid)
        return order


class ReviewListView(generics.ListAPIView):
    """
    List product reviews.

    Using the product Id(eg. 1, 2, 3 etc) you will get the reviews
    on that product
    """

    serializer_class = ReviewSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        """
        Retrieve reviews by product_id.
        """
        product_id = self.kwargs["product_id"]

        product = Product.objects.get(id=product_id)
        reviews = Review.objects.filter(product=product)
        return reviews


class CreateReviewView(generics.CreateAPIView):
    """
    Create a new product review.

    Add a review to a product
    """

    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        """
        Create a new product review
        """
        payload = request.data

        user_id = payload["user"]
        product_id = payload["product"]
        rating = payload["rating"]
        review = payload["review"]

        user = User.objects.get(id=user_id)
        product = Product.objects.get(id=product_id)

        Review.objects.create(user=user, product=product, rating=rating, review=review)

        return Response(
            {"message": "Review has been Created Successfully."},
            status=status.HTTP_201_CREATED,
        )


class SearchProductView(generics.ListAPIView):
    """
    Search for Product

    If product exist you will get its details,if not
    you will get an empty response
    """

    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self, *args, **kwargs):
        query = self.kwargs["query"]
        print("query =======", query)

        products = Product.objects.filter(status="published", title__icontains=query)
        return products


class ProductFAQCreateView(generics.CreateAPIView):
    """
    Ask a question about a product.

    Post your question to a product
    """

    permission_classes = (AllowAny,)
    queryset = ProductFAQ.objects.all()
    serializer_class = ProductFAQSerializer

    def perform_create(self, serializer):
        """
        Set the user field to the requesting user.
        """
        serializer.save(user=self.request.user)


class ProductFAQUpdateView(generics.UpdateAPIView):
    """
    Update an existing FAQ for a product.

    Update your question about a product
    """

    permission_classes = (AllowAny,)
    queryset = ProductFAQ.objects.all()
    serializer_class = ProductFAQSerializer

    def get_object(self, *args, **kwargs):
        """
        Ensure the user owns the FAQ before updating.
        """
        faq = super().get_object()
        if faq.user != self.request.user:
            return Response(
                {"error": "You can only update your own FAQs"},
                status=status.HTTP_403_FORBIDDEN,
            )
        return faq


class ProductFAQDeleteView(generics.DestroyAPIView):
    """
    Delete an existing FAQ for a product.

    Remove your question from Frequently asked questions about the product
    """

    permission_classes = (IsAuthenticated,)
    queryset = ProductFAQ.objects.all()
    serializer_class = ProductFAQSerializer

    def get_object(self):
        """
        Ensure the user owns the FAQ before deleting.
        """
        faq = super().get_object()
        if faq.user != self.request.user:
            return Response(
                {"error": "You can only delete your own FAQs"},
                status=status.HTTP_403_FORBIDDEN,
            )
        return faq

    def perform_destroy(self, instance):
        """
        Custom logic for deleting the FAQ instance.
        """
        instance.delete()
        return Response(
            {"message": "FAQ deleted successfully"}, status=status.HTTP_200_OK
        )
