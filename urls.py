from django.urls import path
from chatbot_app import views, profile, user_appointment, fixed_appointment, chat, prescription

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact_us, name='contact_us'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('chat/', chat.chat_page, name='chat_page'),
    path('get_doctor_list/', user_appointment.get_doctor_list, name='get_doctor_list'),
    path('get_doctor_timing/', user_appointment.get_doctor_timing, name='get_doctor_timing'),
    path('prescription/', prescription.prescription, name='prescription'),
    path('time_check/', user_appointment.time_check, name='time_check'),
    path('profile/', profile.profile, name='profile'),
    path('get_profile/', profile.get_profile, name='get_profile'),
    path('get_user_country/', user_appointment.get_user_country, name='get_user_country'),
    path('scheduled_appointment/', fixed_appointment.scheduled_appointment, name='scheduled_appointment'),
    path('appointment_fix/', fixed_appointment.appointment_fix, name='appointment_fix'),
    path('get_doc_details/', fixed_appointment.get_doc_details, name='get_doc_details'),
]