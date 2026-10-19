from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from admin_dashboard.models import doctor
from chatbot_app.models import profile_data, doc_timing


@login_required(login_url='login')
@csrf_exempt
def get_doctor_list(request):
    if request.method == 'POST':
        try:
            country = request.POST.get('country')
            user_pk = request.POST.get('user_pk')
            data = doctor.objects.filter(country=country)
            data_list = []
            user_exists = profile_data.objects.filter(CustomUser_id=user_pk).exists()
            if user_exists:
                for i in data:
                    data_list.append({'pk': i.pk,
                                      'name': i.name,
                                      'image': i.image,
                                      'qualification': i.qualification,
                                      'workspace': i.workspace})
                context = {
                    'data_list': data_list
                }
                return JsonResponse(context)
            else:
                context = {
                    'status': 'not found',
                }
                return JsonResponse(context)
        except Exception as e:
            context = {
                'status': 'failed',
                'error': str(e)
            }
            return JsonResponse(context)
    return render(request, 'chatbot_app/appointment.html')


@csrf_exempt
def get_user_country(request):
    if request.method == 'POST':
        try:
            user_id = request.POST.get('hidden_id')
            data = profile_data.objects.get(CustomUser_id=user_id)
            country_name = data.country
            context = {
                'country': country_name
            }
            return JsonResponse(context)
        except Exception as e:
            context = {
                'status': 'failed',
                'error': str(e)
            }
            return JsonResponse(context)

@csrf_exempt
def get_doctor_timing(request):
    if request.method == 'POST':
        try:
            pk = request.POST.get('pk')
            date_1 = datetime.now().strftime('%Y-%m-%d')

            date_2 = datetime.now() + timedelta(days=1)
            date_2_mod = date_2.strftime('%Y-%m-%d')

            date_3 = datetime.now() + timedelta(days=2)
            date_3_mod = date_3.strftime('%Y-%m-%d')

            date_4 = datetime.now() + timedelta(days=3)
            date_4_mod = date_4.strftime('%Y-%m-%d')

            date_5 = datetime.now() + timedelta(days=4)
            date_5_mod = date_5.strftime('%Y-%m-%d')

            date_6 = datetime.now() + timedelta(days=5)
            date_6_mod = date_6.strftime('%Y-%m-%d')

            date_7 = datetime.now() + timedelta(days=6)
            date_7_mod = date_7.strftime('%Y-%m-%d')

            day_1 = datetime.now().strftime("%A")
            day_2 = date_2.strftime("%A")
            day_3 = date_3.strftime("%A")
            day_4 = date_4.strftime("%A")
            day_5 = date_5.strftime("%A")
            day_6 = date_6.strftime("%A")
            day_7 = date_7.strftime("%A")
            list = []
            status = 0
            data = doc_timing.objects.filter(doctor_id=pk, status=status)
            days = []
            for i in data:
                list.append({'pk': i.pk,
                             'day': i.day,
                             'timing': i.timing})
            days.append({'date_1': date_1,
                         'date_2': date_2_mod,
                         'date_3': date_3_mod,
                         'date_4': date_4_mod,
                         'date_5': date_5_mod,
                         'date_6': date_6_mod,
                         'date_7': date_7_mod,
                         'day_1': day_1,
                         'day_2': day_2,
                         'day_3': day_3,
                         'day_4': day_4,
                         'day_5': day_5,
                         'day_6': day_6,
                         'day_7': day_7})
            context = {
                'status': 'success',
                'list': list,
                'days': days
            }
            return JsonResponse(context)
        except Exception as e:
            context = {
                'status': 'failed',
                'error': str(e)
            }
            return JsonResponse(context)


# @login_required(login_url='login')
@csrf_exempt
def time_check(request):
    if request.method == 'POST':
        try:
            pk = request.POST.get('pk')

            details = doc_timing.objects.get(pk=pk)
            status = True

            details.status = status
            details.save()

            context = {
                'status': 'success'
            }
            return JsonResponse(context)
        except Exception as e:
            context = {
                'status': 'failed',
                'error': str(e)
            }
            return JsonResponse(context)
    return render(request, 'chatbot_app/scheduled_appointment.html')