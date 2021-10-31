from django.db import models
from django.db.models.deletion import SET_NULL
from django.urls import reverse


class Category(models.Model):
    # db_index пошук в адмінці швидше працює
    name = models.CharField(max_length=200, db_index=True)
    # витягуєм абсолютну урлу гарний урл
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:
        ordering = ('name',)  # упорядковуєм за полем
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:store', args=[self.slug])


class Brand(models.Model):
    # db_index пошук в адмінці швидше працює
    name = models.CharField(max_length=200, db_index=True)
    # витягуєм абсолютну урлу гарний урл
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_brand', args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(
        Category, related_name='products', null=True, on_delete=models.SET_NULL)
    brand = models.ForeignKey(
        Brand, related_name='products', null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    main_photo = models.ImageField(upload_to='products/%Y/%m%d', blank=True)
    photo_1 = models.ImageField(upload_to='products/%Y/%m%d', blank=True)
    photo_2 = models.ImageField(upload_to='products/%Y/%m%d', blank=True)
    photo_3 = models.ImageField(upload_to='products/%Y/%m%d', blank=True)
    description = models.TextField()
    details = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    rait = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])


class Order(models.Model):
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    email = models.EmailField()
    address = models.CharField(max_length=250, null=True)
    postal_code = models.CharField(max_length=20, null=True)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    paid = models.BooleanField(default=False, null=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
