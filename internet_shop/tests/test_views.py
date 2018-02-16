import pytest
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


def create_test_user():
    u1 = User.objects.create_user(username='UserName', password='Password123', email='Test@gmail.com')
    return u1


def create_test_data(is_good=False):
    from internet_shop.models import Category, Good, Colors, Sizes

    category = Category(name="Одежда", url_name="odezhda", parent=None)
    category.save()
    category = get_object_or_404(Category, name=category.name)

    if is_good is True:
        color = Colors(name="Белый")
        color.save()

        size = Sizes(name="XL")
        size.save()

        good = Good(name="Блузка", description="Тест", cost=2000, category=category)
        good.save()
        good = get_object_or_404(Good, name="Блузка")

        good.color = Colors.objects.all()
        good.sizes = Sizes.objects.all()
        good.save()

        good = get_object_or_404(Good, name=good.name)
        size = get_object_or_404(Sizes, name=size.name)
        color = get_object_or_404(Colors, name=color.name)
    else:
        good = None
        color = None
        size = None

    return {'category': category,
            'good': good,
            'color': color,
            'size': size, }


@pytest.mark.django_db
def test_create_user():
    user = create_test_user()
    assert user.username == "UserName"
    assert user.email == "Test@gmail.com"


@pytest.mark.django_db
def test_test_data_category():
    test_data = create_test_data(is_good=False)
    assert test_data['category'].name == "Одежда"
    assert test_data['good'] is None


@pytest.mark.django_db
def test_test_data_good():
    test_data = create_test_data(is_good=True)
    assert test_data['category'].name == "Одежда"
    assert test_data['good'].name == "Блузка"


@pytest.mark.django_db
def test_index_view(client):
    response = client.get('/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_category_view(client):
    test_data = create_test_data(is_good=False)

    response = client.get('/catalog/{}/'.format(test_data['category'].url_name))
    assert response.status_code == 200


@pytest.mark.django_db
def test_good_view(client):
    test_data = create_test_data(is_good=True)

    response = client.get('/good/{}/'.format(test_data['good'].id))
    assert response.status_code == 200


@pytest.mark.django_db
def test_good_add(client):
    from internet_shop.models import UserBasketItems

    test_data = create_test_data(is_good=True)

    response = client.post('/addtobasket/{}/'.format(test_data['good'].id), {
        'color': test_data['color'].id,
        'size': test_data['size'].id,
        'count_of': "20",
    })

    assert response.status_code == 302

    basket = UserBasketItems.objects.first()
    assert basket.count_of == 20


@pytest.mark.django_db
def test_good_add_again(client):
    from internet_shop.models import UserBasketItems

    test_data = create_test_data(is_good=True)

    response = client.post('/addtobasket/{}/'.format(test_data['good'].id), {
        'color': test_data['color'].id,
        'size': test_data['size'].id,
        'count_of': "20",
    })

    assert response.status_code == 302

    basket = UserBasketItems.objects.first()
    assert basket.count_of == 20

    response = client.post('/addtobasket/{}/'.format(test_data['good'].id), {
        'color': test_data['color'].id,
        'size': test_data['size'].id,
        'count_of': "40",
    })

    assert response.status_code == 302

    basket = UserBasketItems.objects.first()
    assert basket.count_of == 60


@pytest.mark.django_db
def test_good_add_fails(client):
    test_data = create_test_data(is_good=True)

    response = client.post('/addtobasket/{}/'.format(test_data['good'].id), {
        'color': test_data['color'].id,
        'size': test_data['size'].id,
    })
    assert response.status_code == 200
    assert str(response.content) == "b'count_of'"

    response = client.get('/addtobasket/{}/'.format(test_data['good'].id), )
    assert response.status_code == 404


@pytest.mark.django_db
def test_basket_view(client):
    from internet_shop.models import UserBasketItems

    response = client.get('/basket/')

    assert response.status_code == 200

    test_data = create_test_data(is_good=True)
    client.post('/addtobasket/{}/'.format(test_data['good'].id), {
        'color': test_data['color'].id,
        'size': test_data['size'].id,
        'count_of': "40",
    })

    response = client.get('/basket/')

    assert response.status_code == 200
    basket = UserBasketItems.objects.first()
    assert basket.count_of == 40
