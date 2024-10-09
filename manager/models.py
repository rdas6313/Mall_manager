from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Mall(models.Model):
    """ Here we define the data model for mall information """
    name = models.CharField(max_length=100)
    address = models.TextField()
    customers = models.ManyToManyField('Customer')
    inventories = models.ManyToManyField('Inventory')
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)


class Inventory(models.Model):
    """ Data model for inventory information """
    name = models.CharField(max_length=100)
    description = models.TextField()
    quantity = models.PositiveIntegerField()


class Store(models.Model):
    """ Data model for Store information """
    name = models.CharField(max_length=100)
    description = models.TextField()
    lease_start = models.DateField(auto_now_add=True)
    lease_end = models.DateField()
    mall = models.ForeignKey(Mall, on_delete=models.CASCADE)


class Employee(models.Model):
    """ Data model for employee data """
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    address = models.TextField()
    mall = models.ForeignKey(Mall, on_delete=models.CASCADE)
    store = models.ForeignKey(
        Store, on_delete=models.CASCADE, null=True, blank=True)


class Customer(models.Model):
    """ Data model for customer data """
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    address = models.TextField()
    last_visit = models.DateField()
