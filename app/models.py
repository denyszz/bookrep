from django.db import models

# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=200)

class Book(models.Model):
    title = models.CharField(max_length=150)
    publish_date = models.DateTimeField()
    in_stock = models.BooleanField(default=True)
    author_id = models.ForeignKey('Author', on_delete=models.CASCADE,default=1)   #Deleting an Author from the database will delete all the associated books.
    
