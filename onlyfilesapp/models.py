from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

class UserRepo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # email = models.CharField(max_length=120)
    is_admin = models.BooleanField(default=False)

    def __unicode__(self):
        return u"%s" % self.user.username
    
    def __str__(self):
        return self.user.username
    


class Repository(models.Model):
    name = models.CharField(max_length=120)
    identifier = models.UUIDField(editable=False, unique=True)
    master_key = models.TextField(null=True)

    def save(self, *args, **kwargs):
        if not self.identifier:
            self.identifier = uuid.uuid4()

        super().save(*args, **kwargs)

    def __unicode__(self):
        return u"%s" % self.name
    
    def __str__(self):
        return self.name
    
    

class User_Repository(models.Model):
    userepo = models.ForeignKey(UserRepo, null=True, on_delete=models.DO_NOTHING)
    repository = models.ForeignKey(Repository, null=True, on_delete=models.CASCADE)
    user_admin = models.BooleanField(default=False)

    def __unicode__(self):
        return u"%s" % self.userepo.name + u" - %s" % self.repository.name
    
    def __str__(self):
        return self.userepo.user.username + "-" + self.repository.name
    

class Files(models.Model):
    name = models.CharField(max_length=120)
    identifier = models.UUIDField(editable=False, unique=True)
    cloud_id = models.TextField(null=True)
    file_text = models.TextField(default="Test")
    file = models.FileField()
    tag = models.CharField(max_length=120, editable=False)

    def save(self, *args, **kwargs):
        if not self.identifier:
            self.identifier = uuid.uuid4()

        super().save(*args, **kwargs)

    def delete(self):
        self.file.delete()
        super().delete()

    def __unicode__(self):
        return u"%s" % self.name
    
    def __str__(self):
        return self.name
    

class Files_Repository(models.Model):
    file = models.ForeignKey(Files, null=True, on_delete=models.CASCADE)
    repository = models.ForeignKey(Repository, null=True, on_delete=models.CASCADE)

    def __unicode__(self):
        return u"%s" % self.file.name + u" - %s" % self.repository.name
    
    def __str__(self):
        return self.file.name + "-" + self.repository.name
    
