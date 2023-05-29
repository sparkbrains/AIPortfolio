from django.db import models

# Create your models here.


class ImageProcessing(models.Model):
     image = models.ImageField(
        upload_to="images/", max_length=254, null=True, blank=True
    )
    
   
class MusicGeneration(models.Model):
     music = models.FileField(
        upload_to="Music/", max_length=254, null=True, blank=True
    )
    

class StockPrediction(models.Model):
     stock_file = models.FileField(
        upload_to="StockPrediction/", max_length=254, null=True, blank=True
    )
    
   