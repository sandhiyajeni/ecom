from django.db import models
from django.contrib.auth.models import User
class Products(models.Model):
    CATEGORY=((1,"MOBILE"),(2,"SHOES"),(3,"CLOTHS"))
    name=models.CharField(max_length=30,verbose_name='products_name')
    price=models.FloatField(verbose_name='products_price')
    cat=models.IntegerField(choices=CATEGORY)
    details=models.CharField(max_length=100)
    is_active=models.BooleanField(default=True)
    pimage=models.ImageField(upload_to='images/')

    def __str__(self):
        return self.name
class Cart(models.Model):
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column='uid')
    pid=models.ForeignKey(Products,on_delete=models.CASCADE,db_column='pid')
    qty=models.IntegerField(default=1)
class Orders(models.Model):
    order_id=models.IntegerField()
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column='uid')
    pid=models.ForeignKey(Products,on_delete=models.CASCADE,db_column='pid')
    qty=models.IntegerField(default=1)


