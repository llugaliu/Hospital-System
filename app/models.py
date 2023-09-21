from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(null=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title


class Doctor(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='doctor_image', null=True)
    phone = models.CharField(max_length=20, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return self.name


class Patient(models.Model):
    name = models.CharField(max_length=50, null=True)
    gender = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=50, null=True)
    address = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return self.name


class Apoiment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    message = models.TextField(null=True, blank=True)
    date = models.DateTimeField()
    time = models.DateTimeField()

    class Meta:
        ordering = ['date', 'time']

    def __str__(self):
        return f'patient {self.patient} make a appoiment with doctor {self.doctor} '
