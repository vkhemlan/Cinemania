from django.db import models
from sorl.thumbnail.fields import ImageWithThumbnailsField
import hashlib

class Movie(models.Model):
    '''Each particular movie with its poster location saved to the database
    and stored in /static/pics/posters'''
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
    '''Each particular room in the cinema, with its capacity given by 
    its number of rows and columns of seats'''
    name = models.CharField(max_length = 255)
    num_rows = models.PositiveIntegerField()
    num_cols = models.PositiveIntegerField()
    
    def __unicode__(self):
        return self.name
        
class Showing(models.Model):
    '''Each particular presentation of a movie on a given room in a date range
    on certain weekdays (e.g.: Titanic on Room A from 05/02/2010 to 06/03/2010
    in Mondays, Thursdays and Fridays at 18:00, tickets cost US$2.50)
    Weekdays are coded in a list of integers (Monday = 1, Tuesday = 2, ...)'''
    movie = models.ForeignKey(Movie)
    room = models.ForeignKey(Room)
    date_start = models.DateField()
    date_end = models.DateField()
    time = models.TimeField()
    price = models.DecimalField(max_digits = 4, decimal_places = 2)
    week_days = models.CommaSeparatedIntegerField(max_length = 20)
    
class ShowingInstance(models.Model):
    '''A particular presentation of a movie on a given date according to
    the Showing rules'''
    showing = models.ForeignKey(Showing)
    date = models.DateField()
    
class Customer(models.Model):
    '''A normal customer, registered to be able to buy tickets online and
    choosing his/her own seat for movies. Also stores the payment information'''
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
    '''A particular order of a given Customer for financial purposes'''
    customer = models.ForeignKey(Customer)
    date = models.DateField()
    amount = models.PositiveIntegerField()
    
class Reserve(models.Model):
    '''A reservation by a user to attend a specific showing of a movie along
    its seat. The reservation is also tied to the buying order'''
    showing_instance = models.ForeignKey(ShowingInstance)
    order = models.ForeignKey(Order)
    row_number = models.PositiveIntegerField()
    col_number = models.PositiveIntegerField()
    
class AdminUser(models.Model):
    '''Information about the manager user, able to insert new movies and
    schedule showings'''
    username = models.CharField(max_length = 255)
    password = models.CharField(max_length = 40)
    
    def validate_user(self):
        if AdminUser.objects.filter(username = self.username).filter(password = hashlib.sha1(self.password).hexdigest()):
            return True
        else:
            return False
