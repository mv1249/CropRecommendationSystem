from django.db import models

# Create your models here.


class CreateUser(models.Model):
    sno = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def __repr__(self):
        return f' {self.sno},{self.fullname},{self.username},{self.password}'
