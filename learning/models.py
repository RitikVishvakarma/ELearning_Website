from django.db import models
from django.utils.timezone import  now
from django.contrib.auth.models import User
# Create your models here.
class Contact(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=12)
    msg = models.TextField()
    timeStamp = models.DateTimeField(auto_now_add=True, blank=True)
    def __str__(self):
        return 'Message from ' +self.name
    
class Subject(models.Model):
    subject_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=500)
    desc = models.CharField(max_length=800)
    slug = models.CharField(max_length=130)
    image = models.ImageField()
    timeStamp = models.DateTimeField(default=now)
    def __str__(self):
        return self.title
    
class Videos(models.Model):
    sno = models.AutoField(primary_key=True)
    title = models.CharField(max_length=500)
    cont = models.TextField()
    vurl = models.URLField(max_length=200)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='videos')
    position = models.PositiveSmallIntegerField(verbose_name="videono.")
    slug = models.CharField(max_length=130)
    timeStamp = models.DateTimeField(default=now)
    def __str__(self):
        return self.title

class VideoComment(models.Model):
    sno = models.AutoField(primary_key=True)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Videos, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return self.comment[0:13] + " by " + self.user.username
    