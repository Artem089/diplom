import random

from demo.forms import RegisterUserForm, ApplicationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import CreateView
from demo.models import Order, Product, Cart, ItemInOrder, Category


# Create your views here.
def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'pages/about.html')


def rate(request):
    return render(request, 'pages/rate.html')


def competitions(request):
    return render(request, 'pages/competitions.html')


def catalog(request):
    return render(request, 'pages/catalog.html')


# Страницы с тарифами
def pageMoskow(request):
    return render(request, 'pages/pageMoskow.html')


def pageCherepovez(request):
    return render(request, 'pages/pageCherepovez.html')


def pageVologda(request):
    return render(request, 'pages/pageVologda.html')


def pageAstana(request):
    return render(request, 'pages/pageAstana.html')


def pageStPetersburg(request):
    return render(request, 'pages/pageStPetersburg.html')


def competitions(request):
    return render(request, 'pages/competitions.html')


class RegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = RegisterUserForm
    context_object_name = 'form'
    success_url = reverse_lazy('login')


def catalog(request):
    category = request.GET.get('category')

    if category:
        products = Product.objects.filter(count__gte=1, category=category)
    else:
        products = Product.objects.filter(count__gte=1)

    order_by = request.GET.get('order_by')

    if order_by:
        products = products.order_by(order_by)
    else:
        products = products.order_by('-date')

    return render(request, 'pages/catalog.html',
                  context={'products': products,
                           'category': Category.objects.all(),
                           })


def product(request):
    return render(request, 'pages/product.html')


def product(request):
    return render(request, 'pages/product.html')


# @login_required
# def checkout(request):
#     return render(request, 'pages/checkout.html')


# class ProductDetail(generic.DetailView):
#     model = Product
#     template_name = "pages/detail.html"


def detail(request, id):
    products = Product.objects.order_by('?')[:4]
    product = get_object_or_404(Product, pk=id)
    print(product.count)
    return render(request, 'pages/detail.html', context={'product': product, 'products': products})


class OrderListView(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = 'pages/orders.html'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-date')


@login_required
def orders(request):
    products = Product.objects.order_by('?')[:4]
    orders_items = Order.objects.filter(user=request.user).order_by('-date')
    totals = []
    if orders_items:
        for i in orders_items:
            total = 0

            for item in i.iteminorder_set.all():
                total += int(item.price)

            totals.append(total)
            print(total)
        orders_items = zip(orders_items, totals)
    return render(request, 'pages/orders.html',
                  context={'order_list': orders_items,
                           'totals': totals, 'products': products})


@login_required
def cart(request):
    products = Product.objects.order_by('?')[:4]
    cart_items = request.user.cart_set.all()
    return render(request, 'pages/cart.html',
                  context={'cart_items': cart_items, 'products': products})


@login_required
def delete_order(request, pk):
    order = Order.objects.filter(user=request.user, pk=pk)
    if order:
        order.delete()
        return redirect('orders')


@login_required
def confirm_order(request, pk):
    order = Order.objects.filter(user=request.user, pk=pk).first()
    if order:
        order.status = 'confirmed'
        order.save()
        return redirect('orders')


@login_required
def to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    item_in_cart = Cart.objects.filter(user=request.user, product=product).first()
    if item_in_cart:
        if item_in_cart.count + 1 > item_in_cart.product.count:
            return JsonResponse({
                'error': 'Нельзя добавить больше'
            })
        item_in_cart.count += 1
        product.count -= 1
        item_in_cart.save()
        product.save()
        return JsonResponse({
            'count': item_in_cart.count
        })
    item_in_cart = Cart(user=request.user, product=product, count=1)
    product.count -= 1
    item_in_cart.save()
    product.save()
    return JsonResponse({
        'count': item_in_cart.count
    })


@login_required
def checkout(request):
    password = request.GET.get('password', None)
    valid = request.user.check_password(password)
    if not valid:
        return JsonResponse({
            'error': 'Не верный пароль'
        })
    item_in_cart = request.user.cart_set.all()
    if not item_in_cart:
        return JsonResponse({
            'error': 'Корзина пуста'
        })
    order = Order.objects.create(user=request.user)
    for item in item_in_cart:
        ItemInOrder.objects.create(order=order, product=item.product,
                                   count=item.count, price=item.count * item.product.price)
    item_in_cart.delete()
    return JsonResponse({
        'message': 'Заказ обработан'
    })


@login_required
def remove_from_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    item_in_cart = Cart.objects.filter(user=request.user, product=product).first()
    if not item_in_cart:
        print(item_in_cart)
        return JsonResponse({
            'error': 'Не найдено'
        })
    item_in_cart.count -= 1
    product.count += 1
    item_in_cart.save()
    product.save()
    if item_in_cart.count == 0:
        item_in_cart.delete()
        return JsonResponse({
            'count': 0
        })
    return JsonResponse({
        'count': item_in_cart.count
    })


def application(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'application/success.html')
    else:
        form = ApplicationForm()
    return render(request, 'application/application.html', {'form': form})
