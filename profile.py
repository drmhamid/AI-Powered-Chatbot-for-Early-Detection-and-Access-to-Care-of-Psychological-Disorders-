from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from authen_app.models import CustomUser
from chatbot_app.models import profile_data
from chatbot_app.views import BASE_DIR


@login_required(login_url='login')
@csrf_exempt
def profile(request):
    if request.method == 'POST':
        try:
            user_id = request.POST.get('hidden_id')
            user_exist = CustomUser.objects.filter(id=user_id).exists()
            if user_exist:
                f_name = request.POST.get('f_name')
                l_name = request.POST.get('l_name')
                gender = request.POST.get('gender2')
                address = request.POST.get('address')
                dob = (request.POST.get('dob')).split("/")
                corrected_dob = (dob[2] + "-" + dob[0] + "-" + dob[1])
                print(corrected_dob)
                city = request.POST.get('city')
                province = request.POST.get('province')
                country = request.POST.get('country')
                profession = request.POST.get('profession')
                education = request.POST.get('education')
                marital_status = request.POST.get('marital_status')
                age = request.POST.get('age')
                image = request.FILES.get('filePhoto')
            else:
                context = {
                    'status': 'failed'
                }
                print(context)
            fs = FileSystemStorage()
            image_save = fs.save(f'{BASE_DIR}/static/profile/' + image.name, image)
            image_url = fs.url(image_save)
            check_data = profile_data.objects.filter(CustomUser_id=user_id).exists()
            if not check_data:
                obj_data = profile_data()
                obj_data.f_name = f_name
                obj_data.l_name = l_name
                obj_data.gender = gender
                obj_data.address = address
                obj_data.dob = corrected_dob
                obj_data.city = city
                obj_data.province = province
                obj_data.country = country
                obj_data.age = age
                obj_data.education = education
                obj_data.profession = profession
                obj_data.marital_status = marital_status
                obj_data.image = image_url
                obj_data.CustomUser_id = user_id
                obj_data.save()
            else:
                obj_data = profile_data.objects.get(CustomUser_id=user_id)
                obj_data.f_name = f_name
                obj_data.l_name = l_name
                obj_data.gender = gender
                obj_data.address = address
                obj_data.dob = corrected_dob
                obj_data.city = city
                obj_data.province = province
                obj_data.country = country
                obj_data.age = age
                obj_data.education = education
                obj_data.profession = profession
                obj_data.marital_status = marital_status
                obj_data.image = image_url
                obj_data.save()
            context = {
                'image_url': image_url
            }
            print(context)
            return render(request, 'chatbot_app/profile.html', context)

        except Exception as e:
            context = {
                'status': 'failed',
                'error': str(e)
            }
        return render(request, 'chatbot_app/profile.html')
    return render(request, 'chatbot_app/profile.html')


@csrf_exempt
def get_profile(request):
    if request.method == 'POST':
        user_id = request.POST.get('hidden_id')
        details = profile_data.objects.filter(CustomUser_id=user_id)
        data_list = []
        for i in details:
            data_list.append({'pk': i.CustomUser_id,
                              'first_name': i.f_name,
                              'last_name': i.l_name,
                              'address': i.address,
                              'province': i.province,
                              'country': i.country,
                              'city': i.city,
                              'gender': i.gender,
                              'dob': i.dob,
                              'education': i.education,
                              'profession': i.profession,
                              'image': i.image,
                              'age': i.age,
                              'marital_status': i.marital_status})
    context = {
        'data_list': data_list
    }
    return JsonResponse(context)
