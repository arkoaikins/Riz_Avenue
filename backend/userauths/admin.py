from django.contrib import admin
from userauths.models import User, Profile


class UserAdmin(admin.ModelAdmin):
    """
    This class configures the display and search functionalities
    within the Django admin interface for User Objects

    List View:
        Displays: full_name, email, phone
        Allows searching by username, full name, email and phone for
            for efficient user lookup
    """

    list_display = ["full_name", "email", "phone"]
    search_fields = ["username", "full_name", "email", "phone"]


class ProfileAdmin(admin.ModelAdmin):
    """
    This class configures the display, search and filtering functionalities
    within the Django admin interface for Profile retrieval

    List View:
        Displays: full_name, gender, country
        Allows searching by state, full name, gender, and country
            for easy profile retrieval
    """

    list_display = ["full_name", "gender", "country"]
    search_fields = ["state", "full_name", "gender", "country"]
    list_filter = ["date"]


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
