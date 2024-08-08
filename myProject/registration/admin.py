from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import CustomRegistrationForm
from .models import CustomUser
from main.models import Product, Category

from main.forms import ProductForm


class CustomUserAdmin(BaseUserAdmin):
    model = CustomUser
    add_form = CustomRegistrationForm
    list_display = ('username', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions', 'groups')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name', 'is_active', 'is_staff'),
        }),
    )
    search_fields = ('username',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = ('name','image')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    add_form = ProductForm
    list_display = ('image','name', 'category', 'price')
    fieldsets = (
        ('Image', {'fields': ('image','category')}),
        (None, {'fields': ('name', 'price')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
