from django.shortcuts import render, redirect
from .models import Category, Patient, Apoiment, Doctor
from .forms import SignUpForm, AppoimentForm, DoctorForm, PatientForm, CategoryForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from datetime import datetime
from datetime import datetime, timedelta
import time


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You created an account')
            return redirect('login')
    else:
        form = SignUpForm
    return render(request, 'base/signup.html', {'form': form})


@login_required(login_url='login')
def home(request):
    categories = Category.objects.all()
    appoiment = Apoiment.objects.all()
    doctors = Doctor.objects.all()
    if 'q' in request.GET:
        q = request.GET['q']
        doctors = Doctor.objects.filter(
            Q(category__title__icontains=q)

        )
    else:
        categories = Category.objects.all()
    paginator = Paginator(doctors, 8)
    page = request.GET.get('page')
    all_doctors = paginator.get_page(page)
    context = {
        'categories': categories,
        'appoiment': appoiment,
        'doctors': all_doctors
    }
    return render(request, 'app/index.html', context)


@login_required(login_url='login')
def doctor(request):
    if 'q' in request.GET:
        q = request.GET['q']
        doctors = Doctor.objects.filter(
            Q(name__icontains=q) |
            Q(phone__icontains=q) |
            Q(category__title__icontains=q)

        )
    else:
        doctors = Doctor.objects.all()
    paginator = Paginator(doctors, 12)
    page = request.GET.get('page')
    all_doctors = paginator.get_page(page)
    count_doctor = doctors.count()
    count_category = Category.objects.all().count()
    context = {
        'doctors': all_doctors,
        'count_doctor': count_doctor,
        'count_category': count_category
    }
    return render(request, 'app/doctor.html', context)


@login_required(login_url='login')
def add_doctor(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        form = DoctorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'You added a doctor')
            return redirect('doctor')
    else:
        form = DoctorForm()
    return render(request, 'app/doctor_form.html', {'form': form, 'categories': categories})


@login_required(login_url='login')
def edit_doctor(request, pk):
    doctor = Doctor.objects.get(id=pk)
    categories = Category.objects.all()
    form = DoctorForm(instance=doctor)
    if request.method == 'POST':
        form = DoctorForm(request.POST, request.FILES, instance=doctor)
        if form.is_valid():
            form.save()
            messages.success(request, f'You updated doctor {doctor}')
            return redirect('doctor')
    else:
        form = DoctorForm(instance=doctor)
    return render(request, 'app/edit_doctor.html', {'form': form, 'categories': categories, 'doctor': doctor})


@login_required(login_url='login')
def delete_doctor(request, pk):
    doctor = Doctor.objects.get(pk=pk)
    doctor.delete()
    messages.info(request, f'You deleted a doctor {doctor}')
    return redirect('doctor')


@login_required(login_url='login')
def patient(request):
    if 'q' in request.GET:
        q = request.GET['q']
        patients = Patient.objects.filter(
            Q(name__icontains=q) |
            Q(mobile__icontains=q) |
            Q(gender__icontains=q) |
            Q(address__icontains=q)

        )
    else:
        patients = Patient.objects.all()
    paginator = Paginator(patients, 10)
    page = request.GET.get('page')
    all_patients = paginator.get_page(page)
    return render(request, 'app/patient.html', {'patients': all_patients})


@login_required(login_url='login')
def add_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, 'You adedd a patient')
            return redirect('patient')
    else:
        form = PatientForm()
    return render(request, 'app/add_patient.html', {'form': form})


@login_required(login_url='login')
def edit_patient(request, pk):
    patient = Patient.objects.get(pk=pk)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.info(request, 'You updated a patient')
            return redirect('patient')
    else:
        form = PatientForm(instance=patient)
    return render(request, 'app/edit_patient.html', {'form': form, 'patient': patient})


@login_required(login_url='login')
def delete_patient(request, pk):
    patient = Patient.objects.get(pk=pk)
    patient.delete()
    messages.info(request, f'You deleted a patient with name {patient}')
    return redirect('patient')


@login_required(login_url='login')
def appoiment(request):
    appoiments = Apoiment.objects.all()
    paginator = Paginator(appoiments, 10)
    page = request.GET.get('page')
    all_appoiments = paginator.get_page(page)
    return render(request, 'app/appoiment.html', {'appoiments': all_appoiments})


@login_required(login_url='login')
def appoiment_detail(request, pk):
    appoiment = Apoiment.objects.get(id=pk)
    present = appoiment.date.now().timestamp()
    past = appoiment.time.timestamp()
    deadline = (present > past)
    context = {
        'appoiment': appoiment,
        'deadline': deadline
    }
    return render(request, 'app/appoiment_detail.html', context)


@login_required(login_url='login')
def appoiment_form(request, pk):
    doctor = Doctor.objects.get(pk=pk)
    form = AppoimentForm(request.POST)
    if form.is_valid():
        appoiment = form.save(commit=False)
        appoiment.doctor = doctor
        appoiment.save()
        messages.success(request, 'You made it an appoiment')
        return redirect('/')
    context = {
        'form': form,
    }
    return render(request, 'app/appoiment_form.html', context)


@login_required(login_url='login')
def delete_appoiment(request, pk):
    appoiment = Apoiment.objects.get(pk=pk)
    appoiment.delete()
    messages.success(request, 'You deleted an appoiment')
    return redirect('appoiment')


def category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category was added')
            return redirect('/')
    else:
        form = CategoryForm()
    return render(request, 'app/category.html', {'form': form})


def delete_category(request, pk):
    category = Category.objects.get(id=pk)
    category.delete()
    messages.info(request, 'Category Was Deleted')
    return redirect('/')
