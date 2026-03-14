from django.db import models

class SaleProduct(models.Model) :
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=200)
    product_price = models.FloatField(default=0.0)
    product_qty = models.IntegerField(default=0)
    phone_number = models.CharField(max_length=20)
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='product_images/',null=True ,blank=True)
    def __str__(self) :
        return self.product_name
    
class Learning(models.Model)  :
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='learning_images/',null=True, blank=True)
    video = models.FileField(upload_to='learning_videos/' ,null =True , blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title
    
class RicePrice(models.Model) :
    id = models.AutoField(primary_key=True)
    rice_name = models.CharField(max_length=200)
    price_per_kg = models.FloatField(default=0.0)
    phone = models.CharField(max_length=30)
    date = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to='rice_image/',null=True ,blank=True)
    def __str__(self) :
        return self.rice_name

class RiceVarieties(models.Model) :
    product_id = models.AutoField(primary_key=True)
    variety_name = models.CharField(max_length=200)
    price = models.FloatField(default=0.0)
    product_qty = models.FloatField(default=0.0)
    phone= models.CharField(max_length=30)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='rice_varieties_images/',null=True, blank=True)
    def __str__(self) :
        return self.variety_name
