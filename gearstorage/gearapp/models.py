from django.db import models
from django_resized import ResizedImageField

# Create your models here.
class MainCategory(models.Model):
    name = models.CharField(max_length=255)
    order = models.IntegerField()

    def __str__(self):
        return f'{self.name}'

    def __unicode__(self):
        return f'{self.name}'


class ItemCategory(models.Model):
    name = models.CharField(max_length=255)
    order = models.IntegerField()
    maincategory = models.ForeignKey(MainCategory, on_delete=models.CASCADE, verbose_name='name')

    def __str__(self):
        return f'{self.name}'

    def __unicode__(self):
        return f'{self.name}'


class Item(models.Model):
    item_category = models.ForeignKey(ItemCategory, on_delete=models.CASCADE, verbose_name='Sub category')
    brand = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    purchase_date = models.DateField(blank=True, null=True)
    weight = models.IntegerField()
    image = ResizedImageField(size=[286, 180], upload_to='item_images', blank=True, null=True)
    info = models.TextField(blank=True, null=True)
    damaged = models.BooleanField()
    retired = models.BooleanField()


    def __str__(self):
        return f"{self.brand} {self.name}"

