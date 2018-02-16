from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect, reverse

from internet_shop.forms import AddToBasketForm, AddOrderForm
from internet_shop.models import Category, Good, UserBasketItems, ReadyOrder

import uuid


def index_view(request):
    categories = Category.objects.all()
    return render(request, 'internet_shop/index.html', {
        'categories': categories,
        'title': 'My Shop',
    })


def category_view(request, category_name):
    categories = Category.objects.all()
    category = get_object_or_404(Category, url_name=category_name)
    goods = Good.objects.all().filter(category=category)
    return render(request, 'internet_shop/category.html', {
        'title': category.name,
        'categories': categories,
        'goods': goods,
    })


def good_view(request, good_id):
    categories = Category.objects.all()
    form = AddToBasketForm(good_id)
    good = get_object_or_404(Good, id=good_id)
    return render(request, 'internet_shop/good.html', {
        'title': good.name,
        'form': form,
        'categories': categories,
        'good_data': good,
    })


def add_good(request, item_id):
    if request.method == "POST":
        form = AddToBasketForm(item_id, data=request.POST)
        if form.is_valid():
            new_item = form.save(commit=False)
            good = get_object_or_404(Good, id=item_id)

            uid = uuid.uuid4()
            if 'user_id' in request.COOKIES:
                uid = request.COOKIES.get('user_id')

            if (UserBasketItems.objects.filter(
                    uid=uid, good=good).exists()):
                item = get_object_or_404(
                    UserBasketItems,
                    uid=uid,
                    good=good)
                item.count_of += int(request.POST['count_of'])
                item.summ += int(request.POST['count_of']) * good.cost
                item.save()
            else:
                new_item.uid = uid
                new_item.good = good
                new_item.count_of = int(request.POST['count_of'])
                new_item.summ = new_item.count_of * good.cost
                new_item.save()

            response = redirect(basket_view)
            response.set_cookie('user_id', uid)
            return response
        return HttpResponse(form.errors)
    else:
        raise Http404()


def del_good(request, item_id):
    if request.method == "POST":
        busket_good = UserBasketItems.objects.filter(id=item_id, uid=request.COOKIES['user_id']).delete()
        return redirect(reverse('basket_view'))

    else:
        raise Http404()


def basket_view(request):

    categories = Category.objects.all()
    form = AddOrderForm()

    if 'user_id' not in request.COOKIES:
        user_id = uuid.uuid4()
    else:
        user_id = request.COOKIES.get('user_id')

    basket_items = UserBasketItems.objects.filter(uid=user_id)

    response = render(request, 'internet_shop/basket.html', {
        'title': "Корзина",
        'categories': categories,
        'basket_items': basket_items,
        'form': form,
    })
    response.set_cookie('user_id', user_id)
    return response


def ready_view(request):
    if request.method == "POST":
        categories = Category.objects.all()
        order = AddOrderForm(data=request.POST)
        if order.is_valid():
            order.save()
        return render(request, 'internet_shop/ready.html', {
            'title': "Готово!",
            'uid': request.POST['uid'],
            'categories': categories,
        })
    else:
        raise Http404()