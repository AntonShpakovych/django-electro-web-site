from django.contrib.auth.models import User, Group
from django.db.models.fields import EmailField
from django.shortcuts import get_object_or_404, redirect, render
from shop.models import Order, OrderItem
from .models import Profile
from .forms import UserLoginForm, AddProductForm
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from cart.cart import Cart
from shop.models import Product
from django.contrib.auth.decorators import user_passes_test


def log_in(request):
    if request.method == "POST":
        password = request.POST['password']
        username = request.POST['username']
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('shop:home')
        else:
            pass
    return render(request, 'myauth/login.html')


def log_out(request):
    logout(request)
    return redirect('myauth:login')


def sign_in(request):
    if request.method == "POST":
        password = request.POST['password']
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        city = request.POST['city']
        phone = request.POST['phone']
        address = request.POST['address']
        country = request.POST['country']
        zipcode = request.POST['zipcode']
        user = User.objects.create(username=username, password=password,
                                   first_name=firstname, last_name=lastname, email=email, is_active=True)
        user.set_password(password)
        profile = Profile.objects.create(user=user)
        user.profile.city = city
        user.profile.phone = phone
        user.profile.email = email
        user.profile.address = address
        user.profile.country = country
        user.profile.zipcode = zipcode
        profile.save()
        group = Group.objects.get(name='customers')
        group.user_set.add(user)
        user.save()
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('shop:home')
        else:
            pass
    return render(request, 'myauth/signin.html')


def user_page(request, user_id):
    user_profile = get_object_or_404(Profile, user=user_id)
    user = get_object_or_404(User, username=user_profile)
    products_orders = Order.objects.filter(email=user.profile.email)
    list_with_order = []
    for i in products_orders:
        list_with_order.append(i)

    list_with_order_items = []
    for j in list_with_order:
        list_with_order_items.append(OrderItem.objects.filter(order_id=j))
    return render(request, 'myauth/user_page.html', {'user_profile': user_profile, 'user': user, 'orders': list_with_order_items, 'cart': cart(request)})


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


@user_passes_test(lambda u: u.is_staff)
def my_admin_only_view(request, *args, **kwargs):
    my_reverse_order_item = OrderItem.objects.all().order_by('-quantity')
    qery_with_name_quan = []

    for i in my_reverse_order_item:
        qery_with_name_quan.append([i.product, i.quantity])
    print(qery_with_name_quan)
    products_name_list = [qery_with_name_quan[i][0]
                          for i in range(len(qery_with_name_quan))]
    products_quantity_list = [qery_with_name_quan[i][1]
                              for i in range(len(qery_with_name_quan))]
    products = Product.objects.all()
    all_order = Order.objects.all()
    if request.method == 'POST':
        form = AddProductForm(request.POST)
        if form.is_valid():
            form.cleaned_data['category']
            form.cleaned_data['brand']
            form.cleaned_data['name']
            form.cleaned_data['slug']
            form.cleaned_data['main_photo']
            form.cleaned_data['photo_1']
            form.cleaned_data['photo_2']
            form.cleaned_data['photo_3']
            form.cleaned_data['description']
            form.cleaned_data['details']
            form.cleaned_data['price']
            form.cleaned_data['old_price']
            form.cleaned_data['stock']
            form.cleaned_data['available']
            form.cleaned_data['rait']

            form.save()
            return redirect('shop:store')
    else:
        form = AddProductForm()

    return render(request, 'myauth/admin_page.html', {'name': products_name_list,
                                                      'quantity': products_quantity_list,
                                                      'products': products,
                                                      'orders': all_order,
                                                      'form': form})


@user_passes_test(lambda u: u.is_staff)
def change_order(request, order_id):
    order = Order.objects.filter(id=order_id)
    for i in order:
        i.paid = 'True'
        i.save()
    return redirect('myauth:admin_page')
