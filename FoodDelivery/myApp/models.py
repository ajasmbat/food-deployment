
from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Stores(models.Model):
    user =  models.ForeignKey( User, on_delete=models.CASCADE)
    store_name = models.CharField(max_length=50)

    address = models.CharField(max_length=50)





class Listings(models.Model):
    store = models.ForeignKey(Stores, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=50)
    item_picture =  models.ImageField(upload_to="listingimages",blank=False)
    item_description = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField()


    def __str__(self):
        return self.item_name

class Cart(models.Model):
    user =  models.ForeignKey( User, on_delete=models.CASCADE)
    item = models.ForeignKey(Listings,on_delete=models.CASCADE)
    


