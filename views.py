import os
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from chatbot_app.models import contact, profile_data
import json
from django.conf import settings
import asyncio
# Create your views here.
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

@csrf_exempt
def index(request):
    return render(request, 'chatbot_app/index.html')


@csrf_exempt
def contact_us(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            email = request.POST.get('email')
            subject = request.POST.get('msg_subject')
            description = request.POST.get('message')

            obj_contact = contact()
            obj_contact.name = name
            obj_contact.email = email
            obj_contact.subject = subject
            obj_contact.description = description
            obj_contact.save()

            context = {
                'status': 'success',
                'message': 'Your request has been submitted successfully.'
            }
            return JsonResponse(context)
        except Exception as e:
            context = {
                'status': 'failed',
                'error': str(e)
            }
            return JsonResponse(context)
    return render(request, 'chatbot_app/index.html')

# @login_required(login_url='login')
@csrf_exempt
def dashboard(request):
    if request.user.is_superuser:
        return render(request, 'dashboard/admin_dashboard.html')
    return render(request, 'chatbot_app/dashboard.html')
