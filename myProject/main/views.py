from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from .models import Category, Product

# Отображает главную страницу с перечнем всех товаров.
def index(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'main/index.html', context)

def category(request):
    # Отображает страницу со списком всех категорий.
    categories = Category.objects.all()
    data = {'categories': categories}
    return render(request, 'main/categories.html', data)


# Отображает детальную информацию о товаре по его ID.
def product_detail(request, product_id):

    product = get_object_or_404(Product, id=product_id)
    context = {'product': product}
    return render(request, 'main/product_detail.html', context)


# Добавляет товар в корзину и обновляет общую стоимость.
def add_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    total = request.session.get('total', 0.0)

    if product_id in cart:
        cart[product_id]['quantity'] += 1
    else:
        cart[product_id] = {'quantity': 1, 'price': product.price}

    total += product.price
    request.session['total'] = total
    request.session['cart'] = cart

    return redirect('main:cart')

# Отображает содержимое корзины и общую стоимость.
def cart_view(request):
    cart = request.session.get('cart', {})
    total = request.session.get('total', 0.0)
    product_ids = cart.keys()
    products = Product.objects.filter(id__in=product_ids)

    return render(request, 'main/cart.html', {
        'cart': cart,
        'products': products,
        'total': total
    })

def remove_from_cart(request, product_id):
    # Удаляет товар из корзины и обновляет общую стоимость.
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    total = request.session.get('total', 0.0)

    product_id_str = str(product_id)
    # Проверяет, является ли значение словарем в cart
    if product_id_str in cart:
        if isinstance(cart[product_id_str], dict):
            total -= cart[product_id_str]['quantity'] * cart[product_id_str]['price']
            del cart[product_id_str]
            request.session['total'] = total
        else:
            # Отладочное сообщение
            print(f"Unexpected type in cart: {type(cart[product_id_str])}")

    request.session['cart'] = cart

    return redirect('main:cart')

def clear_cart(request):
    # Очищает корзину и общую стоимость в сессии.
    request.session.pop('cart', None)
    request.session.pop('total', None)
    return redirect('main:cart')

def checkout(request):
    # Имитирует процесс покупки и очищает корзину.
    cart = request.session.get('cart', {})
    total = request.session.get('total', 0.0)

    if not cart:
        messages.error(request, "Ваша корзина пуста!")
        return redirect('main:cart')

    # Создание заказа, интеграция с платежной системой и т.д.

    # Очистить корзину
    request.session.pop('cart', None)
    request.session.pop('total', None)

    return render(request, 'main/checkout.html', {
        'total': total,
    })

@login_required
def profile(request):
    # Отображает страницу профиля пользователя.
    user = request.user
    data = {'user': user}
    return render(request, 'main/profile.html', data)

def chat(request):
    # Отображает страницу чата.
    return render(request, 'main/chat.html')
