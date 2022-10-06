from django.contrib import admin
from .models import Artist, Artwork, Artgallery # import the models from models.py
# Register your models here.

admin.site.register(Artist) # this line will add the model to the admin panel
admin.site.register(Artwork)
admin.site.register(Artgallery)
