from django.db import models
from sorl.thumbnail.fields import ImageWithThumbnailsField

class Movie(models.Model):
    name = models.CharField(max_length = 255)
    duration = models.PositiveIntegerField()
    poster = ImageWithThumbnailsField(
        upload_to = 'pics/posters', 
        thumbnail = { 'size': (200, 300) },
        extra_thumbnails =  {
            'icon': { 'size': (100, 150) }
        },
    )
    
    def __unicode__(self):
        return self.name
        
class Room(models.Model):
    name = models.CharField(max_length = 255)
    num_rows = models.PositiveIntegerField()
    num_cols = models.PositiveIntegerField()
    
    def __unicode__(self):
        return self.name
        
class Showing(models.Model):
    movie = models.ForeignKey(Movie)
    room = models.ForeignKey(Room)
    date_start = models.DateField()
    date_end = models.DateField()
    time = models.TimeField()
    price = models.DecimalField(max_digits = 4, decimal_places = 2)
    week_days = models.CommaSeparatedIntegerField(max_length = 20)
    
class ShowingInstance(models.Model):
    showing = models.ForeignKey(Showing)
    date = models.DateField()
    
class Customer(models.Model):
    CC_CHOICES = (
        ('VISA', 'Visa'),
        ('MC', 'MasterCard'),
    )

    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.EmailField()
    password = models.CharField(max_length = 40)
    cc_brand = models.CharField(max_length = 4, choices = CC_CHOICES)
    cc_number = models.CharField(max_length = 16)
    cc_security_code = models.CharField(max_length = 3)
    
class Order(models.Model):
    customer = models.ForeignKey(Customer)
    date = models.DateField()
    amount = models.PositiveIntegerField()
    
class Reserve(models.Model):
    showing_instance = models.ForeignKey(ShowingInstance)
    order = models.ForeignKey(Order)
    row_number = models.PositiveIntegerField()
    col_number = models.PositiveIntegerField()
    
class AdminUser(models.Model):
    username = models.CharField(max_length = 255)
    password = models.CharField(max_length = 40)
    
