from django.db import models

# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=50,unique=True)

    def __str__(self):
        return self.title

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
    images = models.ImageField(upload_to='images/')
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