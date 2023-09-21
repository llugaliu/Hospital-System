from django import forms
from django.forms import ModelForm
from .models import Apoiment, Doctor, Patient, Category
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class DoctorForm(ModelForm):
    class Meta:
        model = Doctor
        fields = '__all__'
        widgets = {
            'phone': forms.TextInput(
                attrs={
                    'style': 'font-size: 20px;',
                    'class': 'rounded form-control',
                    'data-mask': '(+000) 00-000-000'
                }
            ),
            'category': forms.Select(
                attrs={
                    'class': 'border-bg-primary rounded form-control',
                }
            )
        }


class PatientForm(ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'
        widgets = {
            'phone': forms.TextInput(
                attrs={
                    'style': 'font-size: 20px;',
                    'class': 'rounded form-control',
                    'data-mask': '(+000) 00-000-000'
                }
            ),
        }


class AppoimentForm(ModelForm):
    class Meta:
        model = Apoiment
        fields = ['patient', 'message', 'date', 'time']
        widgets = {
            'patient': forms.Select(
                attrs={
                    'class': 'form-control',
                }
            )
        }


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if len(phone) != 17:
            raise forms.ValidationError('Denied! The field is not complete')
        return phone
