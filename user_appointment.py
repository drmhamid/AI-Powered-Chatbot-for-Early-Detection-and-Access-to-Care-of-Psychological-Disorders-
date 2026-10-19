from datetime import datetime, timedelta, date
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

            all_list = []
            false_list = []
            true_list = []
            status = 0
            data = doc_timing.objects.filter(doctor_id=pk).order_by('date')
            days = []
            # for i in data:
            #     all_list.append(i.date)

            # print(len(false_list), len(true_list), len(all_list))
            # print(datetime.now())
            current_date = datetime.now().strftime("%Y%m%d")
            yesterday = date.today() - timedelta(days=1)
            print(yesterday)
            rows = doc_timing.objects.filter(date=yesterday).exists()
            # print(rows)
            if rows:
                rows_to_be_delete = doc_timing.objects.filter(date=yesterday)
                day = None
                timing_list = []
                for i in rows_to_be_delete:
                    day = i.day
                    timing_list.append(i.timing)
                    row_to_be_delete = doc_timing.objects.get(pk=i.pk)
                    row_to_be_delete.delete()
                for doctors_timing in timing_list:
                    obj = doc_timing()
                    obj.day = day
                    obj.timing = doctors_timing
                    obj.doctor_id = pk
                    obj.date = date.today() + timedelta(days=6)
                    obj.save()
            data_list = doc_timing.objects.filter(doctor_id=pk).order_by('date')
            for i in data_list:
                if not i.status:
                    false_list.append({'pk': i.pk,
                                       'day': i.day,
                                       'timing': i.timing,
                                       'date': i.date})
                else:
                    true_list.append({'pk': i.pk,
                                      'day': i.day,
                                      'timing': i.timing,
                                      'date': i.date
                                      })
                all_list.append({'pk': i.pk,
                                 'day': i.day,
                                 'timing': i.timing.strftime("%I:%M %p"),
                                 'date': i.date,
                                 'status': i.status})
            context = {
                'status': 'success',
                'false_list': false_list,
                'true_list': true_list,
                'all_list': all_list,
                'days': days
            }
            return JsonResponse(context)
        except Exception as e:
            print(e)
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