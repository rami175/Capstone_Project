from django.db import models

# Create your models here.
class product(models.Model):
    name = models.CharField(max_length=225)
    description = models.TextField()
    price = models.IntegerField()
    image = models.ImageField(upload_to='static/img')
    
    def __str__(self):
        return f"{self.name} - ({self.price})"