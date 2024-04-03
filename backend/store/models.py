from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils import timezone
from django.dispatch import receiver
from django.utils.text import slugify
from django.db.models.signals import post_save
from brand.models import Brand
from userauths.models import User, Profile


class Category(models.Model):
    """Model representing a category for products."""
    title = models.CharField(max_length=100)
    image = models.FileField(
        upload_to="category", default="category.jpg", null=True, blank=True
    )
    active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["title"]

    def __str__(self):
        return self.title


class Product(models.Model):
    """Model representing a product."""

    STATUS = (
        ("draft", "Draft"),
        ("disabled", "Disabled"),
        ("rejected", "Rejected"),
        ("in_review", "In Review"),
        ("published", "Published"),
    )

    title = models.CharField(max_length=100)
    image = models.FileField(
        upload_to="product", blank=True, null=True, default="product.jpg"
    )
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )
    price = models.DecimalField(
        max_digits=12, decimal_places=2, default=0.00)
    old_price = models.DecimalField(
        max_digits=12, decimal_places=2, default=0.00)
    shipping_amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=0.00)
    stock_qty = models.PositiveIntegerField(default=1)
    in_stock = models.BooleanField(default=True)
    status = models.CharField(
        choices=STATUS,
        max_length=50,
        default="published",
        null=True,
        blank=True
    )
    featured = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
    rating = models.IntegerField(default=0, null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    pid = ShortUUIDField(
        unique=True, length=10, max_length=20, alphabet="abcdefghij123456789"
    )
    slug = models.SlugField(unique=True)
    date = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        """Override the save method to generate a slug."""
        if self.slug is None or self.slug == "":
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def product_rating(self):
        """Calculate the average rating for the product."""
        product_rating = Review.objects.filter(product=self).aggregate(
            avg_rating=models.Avg("rating")
        )
        return product_rating["avg_rating"]

    def rating_count(self):
        """Return the total count of reviews for the product."""
        return Review.objects.filter(product=self).count()

    def picture(self):
        """Return all pictures associated with the product."""
        return Picture.objects.filter(product=self)

    def specification(self):
        """Return all specifications associated with the product."""
        return Specification.objects.filter(product=self)

    def color(self):
        """Return all colors available for the product."""
        return Color.objects.filter(product=self)

    def size(self):
        """Return all sizes available for the product."""
        return Size.objects.filter(product=self)

    def save(self, *args, **kwargs):
        """Override the save method to update the product rating."""
        self.rating = self.product_rating()
        super(Product, self).save(*args, **kwargs)


class Picture(models.Model):
    """Model representing a picture associated with a product."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    image = models.FileField(upload_to="product", default="product  .jpg")
    active = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)
    pic_id = ShortUUIDField(
        length=10, max_length=25, alphabet="abcdefghij123456789")

    def __str__(self):
        return self.product.title


class Specification(models.Model):
    """Model representing a specification for a product."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    content = models.CharField(max_length=1000, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Size(models.Model):
    """Model representing a size option for a product."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(default=0.00, decimal_places=2, max_digits=12)

    def __str__(self):
        return self.name


class Color(models.Model):
    """Model representing a color option for a product."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    color_code = models.CharField(max_length=100, blank=True, null=True)
    image = models.FileField(upload_to="product", blank=True, null=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    """Model representing a shopping cart."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    qty = models.PositiveIntegerField(default=0, null=True, blank=True)
    price = models.DecimalField(
        decimal_places=2, max_digits=12, default=0.00, null=True, blank=True
    )
    sub_total = models.DecimalField(
        decimal_places=2, max_digits=12, default=0.00, null=True, blank=True
    )
    shipping_amount = models.DecimalField(
        decimal_places=2, max_digits=12, default=0.00, null=True, blank=True
    )
    service_fee = models.DecimalField(
        decimal_places=2, max_digits=12, default=0.00, null=True, blank=True
    )
    tax_fee = models.DecimalField(
        decimal_places=2, max_digits=12, default=0.00, null=True, blank=True
    )
    total = models.DecimalField(
        decimal_places=2, max_digits=12, default=0.00, null=True, blank=True
    )
    country = models.CharField(max_length=100, null=True, blank=True)
    size = models.CharField(max_length=100, null=True, blank=True)
    color = models.CharField(max_length=100, null=True, blank=True)
    cart_id = models.CharField(max_length=1000, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cart_id} - {self.product.title}"


class CartOrder(models.Model):
    """Model representing an order made from the shopping cart."""
    PAYMENT_STATUS = (
        ("paid", "Paid"),
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("cancelled", "Cancelled"),
    )

    ORDER_STATUS = (
        ("Pending", "Pending"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    )

    brand = models.ManyToManyField(Brand, blank=True)
    buyer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    sub_total = models.DecimalField(
        default=0.00, max_digits=12, decimal_places=2)
    shipping_amount = models.DecimalField(
        default=0.00, max_digits=12, decimal_places=2)
    tax_fee = models.DecimalField(
        default=0.00, max_digits=12, decimal_places=2)
    service_fee = models.DecimalField(
        default=0.00, max_digits=12, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)

    payment_status = models.CharField(
        max_length=100, choices=PAYMENT_STATUS, default="pending"
    )
    order_status = models.CharField(
        max_length=100, choices=ORDER_STATUS, default="Pending"
    )

    # Discounts given
    original_total = models.DecimalField(
        default=0.00, max_digits=12, decimal_places=2)
    amount_saved = models.DecimalField(
        max_digits=12, decimal_places=2, default=0.00, null=True, blank=True
    )

    # Bio Data
    full_name = models.CharField(max_length=1000, null=True, blank=True)
    email = models.CharField(max_length=1000, null=True, blank=True)
    phone = models.CharField(max_length=1000, null=True, blank=True)

    # Shipping Address
    address = models.CharField(max_length=1000, null=True, blank=True)
    city = models.CharField(max_length=1000, null=True, blank=True)
    state = models.CharField(max_length=1000, null=True, blank=True)
    country = models.CharField(max_length=1000, null=True, blank=True)
    oid = ShortUUIDField(
        length=10, max_length=25, alphabet="abcdefghij123456789")
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.oid

    def get_order_items(self):
        """Return all items in the order."""
        return CartOrderProduct.objects.filter(order=self)


class CartOrderProduct(models.Model):
    """Model representing a product within an order."""
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    sub_total = models.DecimalField(
        max_digits=12, decimal_places=2, default=0.00)
    shipping_amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=0.00)
    service_fee = models.DecimalField(
        default=0.00, max_digits=12, decimal_places=2)
    tax_fee = models.DecimalField(
        default=0.00, max_digits=12, decimal_places=2)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    color = models.CharField(max_length=100, null=True, blank=True)
    size = models.CharField(max_length=100, null=True, blank=True)
    oid = ShortUUIDField(
        length=10, max_length=25, alphabet="abcdefghij123456789")
    date = models.DateTimeField(default=timezone.now)

    # Coupons that can be given
    original_total = models.DecimalField(
        max_digits=12, decimal_places=2, default=0.00)
    amount_saved = models.DecimalField(
        max_digits=12, decimal_places=2, default=0.00, null=True, blank=True
    )

    def __str__(self):
        return self.oid


class ProductFAQ(models.Model):
    """Model representing frequently asked questions about a product."""
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    email = models.EmailField(null=True, blank=True)
    question = models.CharField(max_length=10000, null=True, blank=True)
    answer = models.CharField(max_length=10000, null=True, blank=True)
    active = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    pid = ShortUUIDField(
        unique=True, length=10, max_length=20, alphabet="abcdefghij123456789"
    )

    def __str__(self):
        return self.question

    class Meta:
        verbose_name_plural = "Product FAQs"


class Review(models.Model):
    """Model representing a review for a product."""
    StarRating = (
        (1, "★☆☆☆☆"),
        (2, "★★☆☆☆"),
        (3, "★★★☆☆"),
        (4, "★★★★☆"),
        (5, "★★★★★"),
    )

    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    review = models.TextField()
    reply = models.TextField(null=True, blank=True, max_length=1000)
    rating = models.IntegerField(choices=StarRating, default=None)
    active = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.product:
            return self.product.title

    class Meta:
        verbose_name_plural = "Star Rating & Reviews"

    def profile(self):
        return Profile.objects.get(user=self.user)


@receiver(post_save, sender=Review)
def update_product_rating(sender, instance, **kwargs):
    """Update product rating after saving a review."""
    if instance.product:
        instance.product.save()


class Favorite(models.Model):
    """Model representing a user's favorite product."""
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.title


class Coupon(models.Model):
    """Model representing a coupon for discounts."""
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True)
    used_by = models.ManyToManyField(User, blank=True)
    coupon_code = models.CharField(max_length=1000)
    discount = models.IntegerField(default=1)
    active = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.coupon_code


class Tax(models.Model):
    """Model representing tax rates for different countries."""
    country = models.CharField(max_length=100)
    rate = models.IntegerField(default=2, help_text="numbers are in %, eg: 2%")
    active = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.country

    class Meta:
        verbose_name_plural = "Taxes"
        ordering = ["country"]
