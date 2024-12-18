from django.db import models
from django_resized import ResizedImageField
from django.contrib.auth.models import User


# Create your models here.
class MainCategory(models.Model):
    """
         Главная категория предмета - связь с пользователем
    """

    name = models.CharField(max_length=255)
    order = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.name}'

    def __unicode__(self):
        return f'{self.name}'


class ItemCategory(models.Model):
    """
    Подкатегория предмета. Возможно использование с чеклистами полученными извне
    """
    name = models.CharField(max_length=255)
    order = models.IntegerField()
    maincategory = models.ForeignKey(MainCategory, on_delete=models.CASCADE, verbose_name='name')

    def __str__(self):
        return f'{self.name}'

    def __unicode__(self):
        return f'{self.name}'


class Storage(models.Model):
    """
        Хранилище предметов. Полки, квартиры, склады
    """
    name = models.CharField(max_length=255)
    order = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.name}'


class Item(models.Model):
    """
        Предмет. Облатдает весом, текущим местом хранения, обычным весом хранения и другими свойствами
    """
    item_category = models.ForeignKey(ItemCategory, on_delete=models.CASCADE, verbose_name='Sub category')
    brand = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    purchase_date = models.DateField(blank=True, null=True)
    weight = models.IntegerField()
    image = ResizedImageField(size=[286, 180], upload_to='item_images', blank=True, null=True)
    info = models.TextField(blank=True, null=True)
    damaged = models.BooleanField()
    retired = models.BooleanField()
    current_storage = models.ForeignKey(Storage, related_name="current_storage", on_delete=models.SET_NULL,
                                        verbose_name='Current Storage', blank=True, null=True)
    last_storage = models.ForeignKey(Storage, related_name="last_storage", on_delete=models.SET_NULL,
                                     verbose_name='Last Storage', blank=True, null=True)
    lease_person = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.brand} {self.name}"


class Mission(models.Model):
    """
        Миссия, она же поездка. Контейнер для вещей
    """
    title = models.CharField(max_length=1024)
    date_start = models.DateField()
    duration = models.IntegerField(default=0)
    description = models.TextField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


class MissionItem(models.Model):
    """
        Связь поездки и предметов. Содержит ссылку на саму себя для реализации контейнеров багажа
    """
    mission = models.ForeignKey(Mission, related_name="missiont_item", on_delete=models.CASCADE)
    item = models.ForeignKey(Item, related_name="mission_item_item", on_delete=models.CASCADE)
    storage = models.ForeignKey('self', related_name="mission_item_strorageitem",
                                on_delete=models.SET_NULL, blank=True, null=True)
