from django.db import models
import uuid


class Good(models.Model):

    name = models.CharField(max_length=140)
    description = models.TextField(blank=True)

    image = models.ImageField(upload_to='good_images', blank=True, null=True, default=None)

    cost = models.IntegerField(default=0)

    category = models.ForeignKey('Category', related_name='goods')


class Category(models.Model):

    name = models.CharField(max_length=140, unique=True)
    url_name = models.CharField(max_length=140, unique=True)

    def __str__(self):
        return self.name


class UserBasketItems(models.Model):
    uid = models.UUIDField(default=uuid.uuid4(), editable=False)
    good = models.ForeignKey('Good', related_name='goods_in_basket')
    count_of = models.IntegerField()
    summ = models.IntegerField(default=0)


class ReadyOrder(models.Model):
    uid = models.UUIDField(default=uuid.uuid4(), editable=False)
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=150)
    email = models.EmailField()
    comment = models.TextField(max_length=1000)
