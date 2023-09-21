from django.contrib import admin
from .models import Patient, Doctor, Apoiment, Category

admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Apoiment)
admin.site.register(Category)
