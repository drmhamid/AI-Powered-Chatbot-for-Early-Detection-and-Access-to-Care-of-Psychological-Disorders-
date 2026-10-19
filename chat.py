import asyncio
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from chatbot import settings
from chatbot_app.data import SYMPTOM_FIELDS
from chatbot_app.models import symptom_prediction


async def get_rasa_response(text):
    agent = settings.INTERPRETER
    response = await agent.handle_text(text)
    return response


@login_required(login_url='login')
@csrf_exempt
def chat_page(request):
    if request.method == 'POST':
        input_text = request.POST.get('text')
        response = asyncio.run(get_rasa_response(input_text))
        print(response)
        if request.POST.get('text') == "Yes":
            print(request.POST.get('text'))
            user = request.user
            symptom_data = symptom_prediction.objects.get_or_create(user_id__CustomUser__email=user.email)
            print(symptom_data)
            for symptom in SYMPTOM_FIELDS:
                print(symptom)
                if symptom not in symptom_data.current_data.keys():
                    symptom_data.current_data[symptom] = True if input_text=="Yes" else False
                    if len(SYMPTOM_FIELDS) == symptom_data.keys():
                        symptom_data.update_symptom_status()
                    break

        if request.POST.get('text') == "Ok, No worries":
            user = request.user
            symptom_data = symptom_prediction.objects.filter(user_id__CustomUser__email=user.email).first()
            symptom_data.update_symptom_status()
        context = {
            'response': response
        }
        return JsonResponse(context)
    return render(request, 'chatbot_app/chat.html')
