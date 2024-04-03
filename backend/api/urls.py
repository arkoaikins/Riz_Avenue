from django.urls import path
from userauths import views as userauths_views
from store import views as store_views
from customer import views as customer_views
from brand import views as brand_views
from rest_framework_simplejwt.views import TokenRefreshView

# Define URL patterns
urlpatterns = [
    # Authentication endpoints
    # Define path for obtaining token pairs using MyTokenObtainPairView
    path("user/token/", userauths_views.MyTokenObtainPairView.as_view()),
    # Define path for refreshing access and refresh tokens using TokenRefreshView
    path("user/token/refresh/", TokenRefreshView.as_view()),
    # Define a path for user registeration using RegisterView
    path("user/register/", userauths_views.RegisterView.as_view()),
    # Define a path for user password reset using PasswordResetAPI
    path("user/password-reset/<email>/", userauths_views.PasswordResetAPI.as_view()),
    path("user/password-change/", userauths_views.PasswordChangeApi.as_view()),
    # Define a path for user profie
    path("user/profile/<user_id>", userauths_views.ProfileView.as_view()),
    # Endpoints for the store
    path("category/", store_views.CategoryListView.as_view()),
    path("products/", store_views.ProductListView.as_view()),
    path("products/<slug>/", store_views.ProductDetailView.as_view()),
    path("cart-view/", store_views.CartView.as_view()),
    path("cart-list/<str:cart_id>/<int:user_id>/", store_views.CartListView.as_view()),
    path("cart-list/<str:cart_id>/", store_views.CartListView.as_view()),
    path("cart-detail/<str:cart_id>", store_views.CartDetailView.as_view()),
    path(
        "cart-detail/<str:cart_id>/<int:user_id>/", store_views.CartDetailView.as_view()
    ),
    path(
        "cart-delete/<str:cart_id>/<int:item_id>/<int:user_id>/",
        store_views.CartItemDeleteView.as_view(),
    ),
    path(
        "cart-delete/<str:cart_id>/<int:item_id>/",
        store_views.CartItemDeleteView.as_view(),
    ),
    path("create-order/", store_views.CreateOrderView.as_view()),
    path("checkout/<order_oid>/", store_views.CheckoutView.as_view()),
    path("review/get-reviews/<product_id>/", store_views.ReviewListView.as_view()),
    path("review/create-review/", store_views.CreateReviewView.as_view()),
    path("search/<str:query>/", store_views.SearchProductView.as_view()),
    path(
        "products/creat-faq/<int:product_id>/",
        store_views.ProductFAQCreateView.as_view(),
        name="create_faq",
    ),
    path(
        "products/update-faq/<int:product_id>/<int:pk>/",
        store_views.ProductFAQUpdateView.as_view(),
        name="update_faq",
    ),
    path(
        "products/delete-faq/<int:product_id>/faqs/<int:pk>/",
        store_views.ProductFAQDeleteView.as_view(),
        name="delete_faq",
    ),
    # Endpoints for customers
    path("customer/orders/<user_id>/", customer_views.OrdersView.as_view()),
    path(
        "customer/orders/<user_id>/<order_oid>/",
        customer_views.OrdersDetailView.as_view(),
    ),
    path("customer/favourites/<user_id>/", customer_views.FavouriteView.as_view()),
    # Endpoints for Brands
    path("brand/create-product/", brand_views.ProductCreateView.as_view()),
    path(
        "brand/update-product/<brand_id>/<product_pid>/",
        brand_views.ProductUpdateView.as_view(),
    ),
    path(
        "brand/delete-product/<brand_id>/<product_pid>/",
        brand_views.ProductDeleteView.as_view(),
    ),
    path("brand/stats/<brand_id>/", brand_views.BrandStatsView.as_view()),
    path("brand/monthly-orders/<brand_id>/", brand_views.MonthlyOrders),
    path("brand/monthly-product/<brand_id>/", brand_views.MonthlyAddedProducts),
]
