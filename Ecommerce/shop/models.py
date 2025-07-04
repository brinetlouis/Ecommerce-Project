from django.db import models

class Category(models.Model):
    name=models.CharField(max_length=30)
    description=models.TextField()
    image=models.ImageField(upload_to='categories')
    def __str__(self):
        return self.name



class Product(models.Model):
    name=models.CharField()
    image=models.ImageField(upload_to="products")
    description=models.TextField()
    price=models.IntegerField()
    stock=models.IntegerField()
    available=models.BooleanField(default=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='products')

    def __str__(self):
        return self.name



from django.contrib.auth.models import AbstractUser
from django.db import models
from random import randint
class User(AbstractUser):
    phone=models.IntegerField(default=0)
    address=models.TextField(default="")
    is_verified=models.BooleanField(default=False)
    otp=models.CharField(max_length=20, null=True, blank=True)






    def generate_otp(self):
        otp_number=str(randint(1000,9999))+str(self.id)
        self.otp=otp_number
        self.save()