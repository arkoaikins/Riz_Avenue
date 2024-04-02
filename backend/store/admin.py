from django.contrib import admin


from store.models import (
    Product,
    Category,
    Picture,
    Specification,
    Size,
    Color,
    Cart,
    CartOrder,
    CartOrderProduct,
    Review,
    ProductFAQ,
    Favorite,
    Coupon,
    Tax,
)


class PictureInline(admin.TabularInline):
    """
    Inline class for Picture model in ProductAdmin.
    """

    model = Picture
    extra = 1


class SpecificationInline(admin.TabularInline):
    """
    Inline class for Specification model in ProductAdmin.
    """

    model = Specification
    extra = 1


class ColorInline(admin.TabularInline):
    """
    Inline class for Color model in ProductAdmin.
    """

    model = Color
    extra = 1


class SizeInline(admin.TabularInline):
    """
    Inline class for Size model in ProductAdmin.
    """

    model = Size
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    """
    Admin class for Product model.
    """

    list_display = [
        "title",
        "price",
        "category",
        "shipping_amount",
        "stock_qty",
        "in_stock",
        "brand",
        "featured",
    ]
    list_editable = ["featured"]
    list_filter = ["date"]
    search_fields = ["title"]
    inlines = [PictureInline, SpecificationInline, SizeInline, ColorInline]


class CartAdmin(admin.ModelAdmin):
    """
    Admin class for Cart model.
    """

    list_display = [
        "product",
        "cart_id",
        "qty",
        "price",
        "sub_total",
        "shipping_amount",
        "service_fee",
        "tax_fee",
        "total",
        "country",
        "size",
        "color",
        "date",
    ]


class CartOrderItemsInlineAdmin(admin.TabularInline):
    """
    Inline class for CartOrderProduct model in CartOrderAdmin.
    """

    model = CartOrderProduct


class CartOrderAdmin(admin.ModelAdmin):
    """
    Admin class for CartOrder model.
    """

    search_fields = ["oid", "full_name", "email", "phone"]
    list_editable = ["order_status", "payment_status"]
    list_filter = ["payment_status", "order_status"]
    list_display = [
        "oid",
        "payment_status",
        "buyer",
        "order_status",
        "sub_total",
        "shipping_amount",
        "tax_fee",
        "service_fee",
        "total",
        "amount_saved",
        "date",
    ]
    inlines = [CartOrderItemsInlineAdmin]


class CartOrderProductAdmin(admin.ModelAdmin):
    """
    Admin class for CartOrderProduct model.
    """

    list_editable = ["date"]
    list_display = [
        "brand",
        "product",
        "qty",
        "price",
        "sub_total",
        "shipping_amount",
        "service_fee",
        "tax_fee",
        "total",
        "date",
    ]


class ReviewAdmin(admin.ModelAdmin):
    """
    Admin class for Review model.
    """

    list_editable = ["active"]
    list_editable = ["active"]
    list_display = ["user", "product", "review", "reply", "rating", "active"]


class ProductFaqAdmin(admin.ModelAdmin):
    """
    Admin class for ProductFaq model.
    """

    list_editable = ["active", "answer"]
    list_display = ["user", "question", "answer", "active"]


class CouponAdmin(admin.ModelAdmin):
    """
    Admin class for Coupon model.
    """

    # inlines = [CouponUsersInlineAdmin]
    list_editable = [
        "coupon_code",
        "active",
    ]
    list_display = ["brand", "coupon_code", "discount", "active", "date"]


admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartOrder, CartOrderAdmin)
admin.site.register(CartOrderProduct, CartOrderProductAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(ProductFAQ, ProductFaqAdmin)
admin.site.register(Favorite)
admin.site.register(Coupon, CouponAdmin)
admin.site.register(Tax)
