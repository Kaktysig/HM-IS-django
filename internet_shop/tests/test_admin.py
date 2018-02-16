import pytest
from django.contrib.admin.sites import AdminSite
from django.shortcuts import get_object_or_404

from internet_shop.admin import CategoryAdmin
from internet_shop.models import Category


@pytest.mark.django_db
def test_admin_category_no_parent():
    site = AdminSite()
    category = Category(name="Одежда", url_name="odezhda", parent=None)
    admin_class = CategoryAdmin(Category, site)
    assert admin_class.related_parent(category) is None


@pytest.mark.django_db
def test_admin_category_have_parent():
    parent = Category(name="Одежда", url_name="odezhda", parent=None)
    parent.save()
    parent = get_object_or_404(Category, name=parent.name)

    category = Category(name="Женская", url_name="zhenskaya", parent=parent)
    category.save()
    category = get_object_or_404(Category, name=category.name)

    site = AdminSite()
    admin_class = CategoryAdmin(Category, site)
    assert admin_class.related_parent(category) == parent.name
