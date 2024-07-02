from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from shop.managers import CustomUserManager

# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=50,unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Categories'

class Product(models.Model):
    class RatingChoices(models.IntegerChoices):
        zero = 0
        one = 1
        two = 2
        three = 3
        four = 4
        five = 5

    name = models.CharField(max_length=255)
    description = models.TextField(null=True,blank=True)
    price = models.FloatField()
    rating = models.FloatField(choices=RatingChoices.choices,default=RatingChoices.zero.value)
    discount = models.IntegerField(default=0)
    quantity = models.IntegerField(default=1)
    image = models.ImageField(upload_to='images/',null=True,blank=True)
    category = models.ForeignKey('Category',on_delete=models.CASCADE,related_name='products')


    @property
    def discounted_price(self):
        if self.discount > 0:
            return self.price * (1-self.discount / 100)
        return self.price


    def __str__(self):
        return self.name

class Order(models.Model):
    name = models.CharField(max_length=255,null=True,blank=True)
    email = models.EmailField()
    quantity = models.PositiveIntegerField(default=1)
    product = models.ForeignKey('Product',on_delete=models.CASCADE,related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    name = models.CharField(max_length=155)
    email = models.EmailField()
    body = models.TextField()
    is_possible = models.BooleanField(default=False)
    product = models.ForeignKey('Product',on_delete=models.CASCADE,related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    birth_of_date = models.DateField(null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email



