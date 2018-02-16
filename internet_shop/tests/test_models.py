import pytest
from django.shortcuts import get_object_or_404


@pytest.mark.django_db
def test_category():
    from internet_shop.models import Category

    parent = Category(name="Одежда", url_name="odezhda", parent=None)
    parent.save()
    parent = get_object_or_404(Category, name=parent.name)

    assert parent.get_level() == 0

    category = Category(name="Женская", url_name="zhenskaya", parent=parent)
    category.save()
    category = get_object_or_404(Category, name=category.name)

    assert category.get_level() == 1
