from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from admin_dashboard.models import doctor
from chatbot import settings
from chatbot_app.models import doc_timing, user_appointment, profile_data


# @login_required(login_url='login')
@csrf_exempt
def appointment_fix(request):
    if request.method == 'POST':
        try:
            time_pk = request.POST.get('time_pk')
            doctor_pk = request.POST.get('doctor_pk')
            user_pk = request.POST.get('user_pk')
            # date = request.POST.get('date')
            # date = '2023-03-12'

            user_exists = profile_data.objects.filter(pk=user_pk).exists()
            if user_exists:
                name = user_exists.f_name
                doctor_exists = doctor.objects.filter(pk=doctor_pk).exists()
                email = doctor.email
                if doctor_exists:
                    timing_details = doc_timing.objects.get(pk=time_pk)
                    time = timing_details.timing
                    day = timing_details.day
                    status = timing_details.status

                    i = doc_timing.objects.get(pk=time_pk)
                    status_true = doc_timing.objects.filter(status=1)
                    if status_true:
                        obj_appointment = user_appointment()
                        obj_appointment.user_details_id = user_pk
                        obj_appointment.doctor_details_id = doctor_pk
                        obj_appointment.time = time
                        obj_appointment.day = day
                        obj_appointment.date = i.date
                        obj_appointment.save()
                        appointment_email(email, name, time, day)
                    context = {
                        'status': 'success'
                    }
                    return JsonResponse(context)
                else:
                    context = {
                        'status': 'failed'
                    }
                    return JsonResponse(context)
            else:
                context = {
                    'status': 'failed'
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
def scheduled_appointment(request):
    if request.method == 'POST':
        try:
            pk = request.POST.get('pk')
            appointment_details = user_appointment.objects.filter(user_details_id=pk)
            appointment_list = []
            for i in appointment_details:
                appointment_list.append({'doctor_pk': i.doctor_details_id,
                                         'time_pk': i.pk,
                                         'time': i.time.strftime("%I:%M %p"),
                                         'date': i.date,
                                         'day': i.day})
            context = {
                'status': 'success',
                'appointment_list': appointment_list,
            }
            return JsonResponse(context)
        except Exception as e:
            context = {
                'status': 'failed',
                'error': str(e)
            }
            return JsonResponse(context)
    return render(request, 'chatbot_app/scheduled_appointment.html')


@csrf_exempt
def get_doc_details(request):
    if request.method == 'POST':
        try:
            pk = request.POST.get('pk')
            doc_details = doctor.objects.filter(pk=pk)
            doc_list = []
            for i in doc_details:
                doc_list.append({'pk': i.pk,
                                 'number': i.number,
                                 'name': i.name,
                                 'qualification': i.qualification,
                                 'workspace': i.workspace,
                                 'image': i.image})
            context = {
                'status': 'success',
                'doctor_list': doc_list
            }
            return JsonResponse(context)
        except Exception as e:
            context = {
                'status': 'failed',
                'error': str(e)
            }
            return JsonResponse(context)
    return render(request, 'chatbot_app/scheduled_appointment.html')


def appointment_email(email, name, time, day):
    try:
        subject = 'Appointment Fixation'
        message = f'Your Appointment with patient {name} is fixed on {day} and the timing is {time}.' \
                  f'The patient will show the generated prescription on his/her own behalf.'
        email_address = email
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email_address]
        send_mail(subject, message, email_from, recipient_list)
        return True
    except Exception as e:
        print(e)
        return False


def delete_appointment(request):
    if request.method == 'POST':
        try:
            pk = request.POST.get('pk')

            obj_appointment = user_appointment.objects.get(pk=pk)
            obj_appointment.delete()
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
