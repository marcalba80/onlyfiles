from django.contrib import admin

# Register your models here.
from onlyfilesapp import models

admin.site.register(models.UserRepo)
admin.site.register(models.Repository)
admin.site.register(models.Files)
admin.site.register(models.User_Repository)
admin.site.register(models.Files_Repository)
