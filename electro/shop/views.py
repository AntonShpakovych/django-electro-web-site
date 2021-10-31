from django.shortcuts import render, get_object_or_404
from django.urls.conf import path
from .forms import OrderCreateForm
from shop.models import Product, Brand, Category, OrderItem
from cart.forms import CartAddProductForm
from django.conf import settings
from cart.cart import Cart

from django.core.paginator import Paginator
from django.shortcuts import render


def home_page(request):
    a = cart(request)
    print(a)
    return render(request, 'pages/index.html', {'cart':  cart(request)})


def store_page(request, category_slug=None, brand_slug=None):
    category = None
    brand = None
    categories = Category.objects.all().order_by('id')
    brands = Brand.objects.all()
    global_dict_filter = {
        'brands': brands,
        'categories': categories
    }
    category_id_list = []
    brand_id_list = []
    for c in range(len(global_dict_filter['categories'])):
        if request.POST.get(f"category-{c+1}", False) == 'on':
            category_id_list.append(c+1)
    for b in range(len(global_dict_filter['brands'])):
        if request.POST.get(f'brand-{b+1}', False) == 'on':
            brand_id_list.append(b+1)
    print('category', category_id_list)

    if category_id_list:
        products = Product.objects.filter(
            available=True, category__in=category_id_list)
        print(products[0].category.id)
    elif brand_id_list:
        products = Product.objects.filter(
            available=True, brand__in=brand_id_list)

    elif category_id_list and brand_id_list:
        products = Product.objects.filter(
            available=True, brand__in=brand_id_list, category__in=category_id_list)
    else:
        products = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.objects.filter(category=category.slug)
    cart_product_form = CartAddProductForm()
    paginator = Paginator(products, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    product_count = len(products)
    return render(request, 'pages/store.html', {'category': category,
                                                'global_dict_filter': global_dict_filter,
                                                'products': products,
                                                'page_obj': page_obj,
                                                'cart_product_form': cart_product_form,
                                                # 'cart_items': pr,
                                                'cart': cart(request),
                                                'product_count': product_count})


def store_list_categories(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    brand = None
    Brands = Brand.objects.all()

    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category)
    cart_product_form = CartAddProductForm()
    cart_items = request.session.get(settings.CART_SESSION_ID)
    product = cart_items.keys()
    paginator = Paginator(products, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'pages/store.html', {'category': category,
                                                'categories': categories,
                                                'page_obj': page_obj,
                                                'products': products,
                                                'cart_product_form': cart_product_form,
                                                'cart': cart(request)})


def product_page(request, id, slug):
    product = get_object_or_404(Product, slug=slug, id=id)
    cart_product_form = CartAddProductForm()
    category = get_object_or_404(Category, slug=product.category.slug)
    print(category)
    return render(request, 'pages/product.html', {'product_detail': product,
                                                  'cart_product_form': cart_product_form,
                                                  'cart':  cart(request),
                                                  'category': category})


def checkout_page(request):
    cart_1 = Cart(request)
    user = request.user
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart_1:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # очистка корзины
            cart_1.clear()
            return render(request, 'pages/order_have.html',
                          {'order': order})
    else:
        form = OrderCreateForm(initial={'first_name': user.first_name,
                                        'last_name': user.last_name,
                                        'email': user.profile.email,
                                        'address': user.profile.address,
                                        'postal_code': user.profile.zipcode,
                                        'city': user.profile.city})
    return render(request, 'pages/checkout.html',
                  {'cart': cart(request), 'form': form, 'user': user, 'cart_1': cart_1})


def cart(request):
    cart = request.session.get(settings.CART_SESSION_ID)
    count = 0
    subtotal = 0
    product_list = 0
    if cart:
        cart_values = cart.values()
        for item in cart_values:
            count += item['quantity']
            subtotal += item['quantity'] * float(item['price'])

        cart_items_id = cart.keys()
        product_list = Product.objects.filter(id__in=cart_items_id)
        cart = Cart(request)

    return {'count': count, 'product_list': product_list,  'subtotal': subtotal, 'cart': cart}
