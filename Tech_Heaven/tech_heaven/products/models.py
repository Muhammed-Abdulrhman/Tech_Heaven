from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=25)
    link = models.CharField(max_length=50)
    def __str__(self):
        return self.title

class Product(models.Model):
    picture = models.ImageField(upload_to='products_images')
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    category =  models.ForeignKey(Category, on_delete=models.CASCADE)
    discount = models.IntegerField()
    description = models.CharField(max_length=300)
    def __str__(self):
        return self.name

class Comments(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    content = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.content

class Cart(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.IntegerField()
    total_price = models.IntegerField()