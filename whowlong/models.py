# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from  django.utils import timezone
import csv
from django.http import HttpResponse
import numpy  as np
import logging

#https://stackoverflow.com/questions/17392087/how-to-modify-django-admin-filters-title
#How to modify Django admin filter's title
def custom_titled_filter(title):
    class Wrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance
    return Wrapper

# Create your models here.
'''
---------------------------------------------------------------------------------

Place

'''
    
class Place (models.Model) :
    name = models.CharField(max_length=128,default=u'DEFAULT',unique=False)
    postalAdress = models.TextField(default=u'',unique=False)

    street = models.TextField(max_length=128,default=u'DEFAULT',unique=False)
    city = models.CharField(max_length=128,default=u'DEFAULT',unique=False)
    pays = models.CharField(max_length=128,default=u'DEFAULT',unique=False)
    
    lat = models.FloatField(default=np.nan,null=True,blank=True)
    lon = models.FloatField(default=np.nan,null=True,blank=True)

    def __str__(self):
        return unicode(self).encode('utf-8')
    
    def __unicode__(self):
        return u"%s " % (self.name)
    
class PlaceAdmin (admin.ModelAdmin) :
    """
    Pour le site d'administration
    """
    
    list_display = (u'name',  u'postalAdress', u'lat', u'lon', u'street',u'city', u'pays')
    list_filter = ('city',u'name')  
            
            
'''
---------------------------------------------------------------------------------

Request

'''

class Request (models.Model):
    log = logging.getLogger(__name__)
    
    user = models.ForeignKey(User,unique=False,on_delete=models.CASCADE)
    submitDate = models.DateTimeField(unique=False,default=timezone.now)
    name =  models.CharField(max_length=128,default=u'DEFAULT',unique=True)
    searchPattern =  models.CharField(max_length=256,default=u'DEFAULT',unique=False)
    origin = models.ForeignKey(Place,unique=False,null=True,on_delete=models.CASCADE,related_name='origin_of_request')
    metersArround =  models.IntegerField(default = 10000)
    places = models.ManyToManyField(Place,related_name='requests')

    def printPlacesArround (self):
        
        print (str(self))
        print ("found %.1f places "%len(self.places.all()))
        for ele in self.places.all() :
            print ( " - %s " % ele)
    
    def __str__(self):
        return unicode(self).encode('utf-8')
    
    def __unicode__(self):  
        return u"%s %d m autour de %s " % (self.name,
                                                self.metersArround, 
                                               self.origin.name)
    
    

class PlaceInline(admin.TabularInline):
    
    model = Request.places.through
    extra = 0 # how many rows to show
    #fk_name = 'places'


class RequestAdmin (admin.ModelAdmin) :
    list_display = (u'user',u'submitDate',  u'name', u'origin','metersArround')
    inlines = [PlaceInline]    

    list_filter = ('user',u'submitDate')
    
    
'''
---------------------------------------------------------------------------------

Trajet

'''    
class Trajet (models.Model):    
    name =  models.CharField(max_length=128,default=u'DEFAULT',unique=True)
    type =  models.CharField(max_length=128,default=u'CAR')
    fromPlace = models.ForeignKey(Place,unique=False,on_delete=models.CASCADE,related_name=u'fromPlace_of_Trajet')
    toPlace = models.ForeignKey(Place,unique=False,on_delete=models.CASCADE,related_name=u'toPlace_of_Trajet')


    def __str__(self):
        return unicode(self).encode('utf-8')
    
    def __unicode__(self):  
        return u"%s" % (self.name)

    
class TrajetAdmin (admin.ModelAdmin) :
    list_display = (u'name',  u'fromPlace', u'toPlace')
    list_filter = (u'fromPlace',u'toPlace')
    
    
    
'''
---------------------------------------------------------------------------------

TrajetData

'''   
class TrajetData (models.Model):    
    #user = models.ForeignKey(User,unique=False,on_delete=models.CASCADE)
    #request =  models.ForeignKey(Request,unique=False,on_delete=models.CASCADE)
    trajet = models.ForeignKey(Trajet,unique=False,on_delete=models.CASCADE)
    trajetDate = models.DateTimeField(unique=False,default=timezone.now)
    distanceKm = models.FloatField(default=0.0)
    dureeMinute = models.IntegerField(default=0)
    trajetDateHeure=models.IntegerField(default=0)
    trajetDateMinute=models.IntegerField(default=0)
    trajetWeekDay =models.IntegerField(default=0)
    computer =  models.CharField(max_length=128,default=u'WAZE')
    
    def display_from(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return self.trajet.fromPlace.name
    display_from.short_description = 'tt From'
    display_from.admin_order_field = 'trajet__fromPlace'    

    def display_to(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return self.trajet.toPlace.name
    display_to.short_description = 'tt To'
    display_to.admin_order_field = 'trajet__toPlace'    
    def __str__(self):
        return unicode(self).encode('utf-8')
    
    def __unicode__(self):  
        return u"%s => %s : %d min %.1f km" % (self.trajet.fromPlace.name,
                                               self.trajet.toPlace.name, 
                                               self.dureeMinute,
                                               self.distanceKm)
class TrajetDataAdmin (admin.ModelAdmin) :
    
    actions = ["export_as_csv"]
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)
        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])
        return response

    export_as_csv.short_description = "Export Selected"

    
    list_display = ( u'trajet', u'display_from',u'display_to',u'trajetDate',u'distanceKm',u'dureeMinute')
    #list_filter = ( u'trajet__fromPlace__name',u'trajet__toPlace__name',u'distanceKm',u'dureeMinute')
    list_filter = ( (u'trajet__fromPlace__name',custom_titled_filter('From')),
                    (u'trajet__toPlace__name',custom_titled_filter('To')),
                    u'distanceKm',u'dureeMinute')
              
    ('fieldname', custom_titled_filter('My Custom Title')),
    
    
    
''' -----------------------------------------------------------
    
   Admin params.
   
   ------------------------------------------------------------
'''

class Param (models.Model) :
    key = models.CharField(max_length=128,default=u'DEFAULT',unique=True)
    value = models.CharField(max_length=128,default=u'XXXX')

    def __str__(self):
        return unicode(self).encode('utf-8')
    
    def __unicode__(self):  
        return u"%s = %s" % (self.key, self.value)

class ParamAdmin (admin.ModelAdmin) : 
    list_display = ('key', 'value')






''' -----------------------------------------------------------
    
   Events, loguer, les evenements.
   
   ------------------------------------------------------------
'''
   
class Event(models.Model):
    user = models.ForeignKey(User,unique=False)
    type = models.CharField(max_length=128,default=u'DEFAULT',unique=False)
    message = models.TextField(default=u'',unique=False)
    date = models.DateTimeField(u'eventDate',unique=False)
    def __unicode__(self):  
        return u"%s %s %s" % (self.user, self.message, self.date)
    def __str__(self):
        return unicode(self).encode('utf-8')
    
class EventAdmin(admin.ModelAdmin):
    list_display = ('type',  'message',u'date','user')
    list_filter = ('date','type','user')    
    
    
def print_agsp_models():
    print (u'********************************************')
    print (u'print_agsp_models()')
    i = 0
    print ("  Place")
    for place in Place.objects.all() :
        i = i + 1
        print ("    %d place %s"%(i,place))
    i = 0
    print ("  Requests")
    for req in Request.objects.all() :
        i = i + 1
        print ("    %d request %s"%(i,req))
    
    
    i = 0
    print ("  Trajets")
    for trajet in Trajet.objects.all() :
        i = i + 1
        print ("    %d trajet %s"%(i,trajet))
        
    