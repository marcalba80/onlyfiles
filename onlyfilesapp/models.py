from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserRepo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=120)
    is_admin = models.BooleanField(default=False)

    def __unicode__(self):
        return u"%s" % self.user.username


class Repository(models.Model):
    name = models.CharField(max_length=120, unique=True)
    master_key = models.TextField()

    def __unicode__(self):
        return u"%s" % self.name
    

class User_Repository(models.Model):
    userepo = models.ForeignKey(UserRepo, null=True, related_name='Usuari')
    repository = models.ForeignKey(Repository, null=True, related_name='Repository')
    user_admin = models.BooleanField(default=False)

    def __unicode__(self):
        return u"%s" % self.userepo.name + u" - %s" % self.repository.name

class Files(models.Model):
    name = models.CharField(max_length=120, unique=True)
    id = models.TextField()

    def __unicode__(self):
        return u"%s" % self.name

class Files_Repository(models.Model):
    file = models.ForeignKey(Files, null=True, related_name='File')
    repository = models.ForeignKey(Repository, null=True, related_name='Repository')

    def __unicode__(self):
        return u"%s" % self.file.name + u" - %s" % self.repository.name
