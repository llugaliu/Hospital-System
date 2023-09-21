from django.urls import path
from django.contrib.auth import views as auth_view
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_view.LoginView.as_view(template_name='base/login.html'), name='login'),
    path('logout/', auth_view.LogoutView.as_view(), name='logout'),
    path('doctor/', views.doctor, name='doctor'),
    path('add-doctor/', views.add_doctor, name='add-doctor'),
    path('edit-doctor/<str:pk>/', views.edit_doctor, name='edit-doctor'),
    path('delete-doctor/<str:pk>/', views.delete_doctor, name='delete-doctor'),
    path('patient/', views.patient, name='patient'),
    path('add-patient/', views.add_patient, name='add-patient'),
    path('edit-patient/<str:pk>/', views.edit_patient, name='edit-patient'),
    path('delete-patient/<str:pk>/', views.delete_patient, name='delete-patient'),
    path('appoiment/', views.appoiment, name='appoiment'),
    path('appoiment-detail/<str:pk>/',
         views.appoiment_detail, name='detail-appoiment'),
    path('add-appoiment/<str:pk>/', views.appoiment_form, name='add-appoiment'),
    path('delete-appoiment/<str:pk>/',
         views.delete_appoiment, name='delete-appoiment'),
    path('category/', views.category, name='category'),
    path('delete-category/<str:pk>/',
         views.delete_category, name='delete-category')
]
