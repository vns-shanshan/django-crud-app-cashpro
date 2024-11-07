from django.contrib import admin
from .models import Transaction, Profile, Comment

# Register your models here.
admin.site.register(Transaction)
admin.site.register(Profile)
admin.site.register(Comment)