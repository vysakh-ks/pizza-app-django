from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Pizza(models.Model):
    sno = models.AutoField(primary_key=True)
    pizza_name = models.CharField(max_length=100)
    pizza_desc = models.TextField()
    pizza_price = models.FloatField()
    image_url = models.URLField(default="")

    def __str__(self):
        return self.pizza_name
    
class Order(models.Model):
    pizza_name = models.CharField(max_length=100)
    pizza_desc = models.TextField()
    pizza_price = models.FloatField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    order_confirmed = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.pizza_name
    
class Profile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    profile_image = models.ImageField(upload_to="images",default="images/defaultuser.png",blank=True,null=True)

    def __str__(self):
        return self.user.username

class Address(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    address = models.TextField(max_length=100)

    def __str__(self):
        return self.user.username


class Contact(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    query = models.TextField()

    def __str__(self):
        return self.user.username
    
    