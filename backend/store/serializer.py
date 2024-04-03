from rest_framework import serializers
from store.models import (
    Category,
    Product,
    Picture,
    Specification,
    Size,
    Color,
    Cart,
    CartOrder,
    CartOrderProduct,
    ProductFAQ,
    Review,
    Favorite,
    Coupon,
)
from brand.models import Brand


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model.
    """

    class Meta:
        model = Category
        fields = "__all__"


class PictureSerializer(serializers.ModelSerializer):
    """
    Serializer for the Picture model.
    """

    class Meta:
        model = Picture
        fields = "__all__"


class SpecificationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Specification model.
    """

    class Meta:
        model = Specification
        fields = "__all__"


class SizeSerializer(serializers.ModelSerializer):
    """
    Serializer for the Size model.
    """

    class Meta:
        model = Size
        fields = "__all__"


class ColorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Color model.
    """

    class Meta:
        model = Color
        fields = "__all__"


class CartSerializer(serializers.ModelSerializer):
    """
    Serializer for the Cart model
    """

    class Meta:
        model = Cart
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the Product model.
    """

    picture = PictureSerializer(many=True, read_only=True)
    color = ColorSerializer(many=True, read_only=True)
    specification = SpecificationSerializer(many=True, read_only=True)
    size = SizeSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "image",
            "description",
            "category",
            "price",
            "old_price",
            "shipping_amount",
            "stock_qty",
            "in_stock",
            "status",
            "featured",
            "views",
            "rating",
            "brand",
            "picture",
            "color",
            "specification",
            "size",
            "product_rating",
            "rating_count",
            "pid",
            "slug",
            "date",
        ]

    def __init__(self, *args, **kwargs):
        """
        Initialize ProductSerializer.
        """
        super(ProductSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3


class CartSerializer(serializers.ModelSerializer):
    """
    Serializer for the Cart model.
    """

    class Meta:
        model = Cart
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(CartSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3


class CartOrderProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the CartOrderProduct model.
    """

    class Meta:
        model = CartOrderProduct
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(CartOrderProductSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3


class CartOrderSerializer(serializers.ModelSerializer):
    """
    Serializer for the CartOrder model.
    """

    get_order_items = CartOrderProductSerializer(many=True, read_only=True)

    class Meta:
        model = CartOrder
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(CartOrderSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3


class ProductFAQSerializer(serializers.ModelSerializer):
    """
    Serializer for the ProductFAQ model.
    """

    class Meta:
        model = ProductFAQ
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(ProductFAQSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3


class BrandSerializer(serializers.ModelSerializer):
    """
    Serializer for the Brand model.
    """

    class Meta:
        model = Brand
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(BrandSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for the Review model.
    """

    class Meta:
        model = Review
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(ReviewSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3


class FavouriteSerializer(serializers.ModelSerializer):
    """
    Serializer for the Favorite model.
    """

    class Meta:
        model = Favorite
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(FavouriteSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3


class CouponSerializer(serializers.ModelSerializer):
    """
    Serializer for the Coupon model.
    """

    class Meta:
        model = Coupon
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(CouponSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3


class BrandStatsSerializer(serializers.Serializer):
    """
    Serializer for the BrandStats model.
    """

    products = serializers.IntegerField()
    orders = serializers.IntegerField()
    income = serializers.DecimalField(max_digits=10, decimal_places=2)
