from django.db import models


class Product(models.Model):
    autor = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    start_date = models.DateTimeField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    max_in_group = models.IntegerField()
    min_in_group = models.IntegerField()

    def __str__(self):
        return self.name


class Lesson(models.Model):
    name = models.CharField(max_length=128)
    link = models.CharField(max_length=128)
    product = models.ForeignKey(to=Product, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=128)
    product = models.ForeignKey(to=Product, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class User(models.Model):
    name = models.CharField(max_length=128)
    group = models.ManyToManyField(to=Group, blank=True, default="not in group")
    product = models.ManyToManyField(to=Product, symmetrical=False, default="no have")

    def __str__(self):
        return self.name
