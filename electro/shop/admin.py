from django.contrib import admin
from shop.models import Category, Brand, Product, Order, OrderItem


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)


class CategoryBrand(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Brand, CategoryBrand)


class CategoryProduct(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price',
                    'old_price', 'rait', 'stock', 'available', 'created', 'updated']
    list_filter = ['rait', 'available', 'created', 'updated']
    list_editable = ['price', 'old_price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Product, CategoryProduct)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email',
                    'address', 'postal_code', 'city', 'paid',
                    'created', 'updated']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)
