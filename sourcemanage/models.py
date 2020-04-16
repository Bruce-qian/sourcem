from django.db import models

# Create your models here.
class User(models.Model):
    acc = models.CharField(max_length=6, primary_key=True, null=False)
    na = models.CharField(max_length=16, null=False)
    paw = models.CharField(max_length=256, null=False)#后面注释掉掉 用不到
    sex = models.IntegerField()
    offer = models.CharField(max_length=20)
    part = models.CharField(max_length=16)
    auth = models.IntegerField()

class Metr(models.Model):
    mid = models.CharField(max_length=6, primary_key=True, null=False)
    size = models.IntegerField()
    sta = models.IntegerField()
    tim = models.DateTimeField()
    lot = models.CharField(max_length=50)
    dis = models.CharField(max_length=50)
    img = models.ImageField()

class Car(models.Model):
    cid = models.CharField(max_length=6, primary_key=True, null=False)
    cflag = models.CharField(max_length=16, null=False)
    sta = models.IntegerField()
    tim = models.DateTimeField()
    chetime = models.DateTimeField()
    comtime = models.DateTimeField()
    suretime = models.DateTimeField()
    size = models.IntegerField()
    img = models.ImageField()

class Carord(models.Model):
    id = models.AutoField(primary_key=True)
    acc = models.ForeignKey(User, on_delete=models.CASCADE)
    cid = models.ForeignKey(Car, on_delete=models.CASCADE)
    stime = models.DateTimeField()
    etime = models.DateTimeField()
    foor = models.CharField(max_length=50)
    drever = models.CharField(max_length=16)
    time = models.DateTimeField()
    sta = models.IntegerField()

class Metorder(models.Model):
    id = models.AutoField(primary_key=True)
    acc = models.ForeignKey(User, on_delete=models.CASCADE)
    mid = models.ForeignKey(Metr, on_delete=models.CASCADE)
    stime = models.DateTimeField()
    etime = models.DateTimeField()
    foor  = models.CharField(max_length=50)
    time = models.DateTimeField()
    sta = models.IntegerField()