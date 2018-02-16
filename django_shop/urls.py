"""django_shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

from internet_shop.views import index_view, category_view, good_view, basket_view, add_good, ready_view, del_good

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # OUR:
    url(r'^$', index_view, name='home'),
    url(r'catalog/(?P<category_name>\w+)/$', category_view, name="category"),
    url(r'basket/$', basket_view, name="basket_view"),
    url(r'addtobasket/(?P<item_id>\d+)/$', add_good, name="basket_add"),
    url(r'deletefrombasket/(?P<item_id>\d+)/$', del_good, name="basket_del"),
    url(r'good/(?P<good_id>\w+)/$', good_view, name="good"),
    url(r'thanks/', ready_view, name='ready'),
]

if settings.DEBUG is True:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT,
    )
