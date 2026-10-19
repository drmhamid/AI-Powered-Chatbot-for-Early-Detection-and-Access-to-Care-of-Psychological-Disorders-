from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from chatbot import settings
from chatbot_app.models import symptom_prediction
import numpy as np

@login_required(login_url='login')
@csrf_exempt
def prescription(request):
    if request.method == 'POST':
        pk = request.POST.get('pk')
        symptom_list = []
        user_exists = symptom_prediction.objects.get(user_id=pk)
        if user_exists:
            for i in user_exists:
                symptom_list.append([i.insomnia, i.fatigue, i.anger, i.stomach_issues,
                                     i.suicidal_thoughts, i.lost_in_interest, i.uneasiness,
                                     i.nausea, i.dizziness, i.heart_palpitations,
                                     i.muscle_ache, i.mood_swings, i.paranoia,
                                     i.neglected_hygiene, i.erratic_behavior, i.relationship_problems,
                                     i.vivid_flashbacks, i.nightmares, i.intrusive_thoughts,
                                     i.avoidance, i.repeating_questions, i.difficulty_concentrating,
                                     i.acting_impulsively, i.movement_issues])
                symptom_array = np.asarray(symptom_list)
                reshaped_array = symptom_array.reshape(1, -1)
                model = settings.model
                prediction = model(reshaped_array)
                print(prediction)
    return render(request, 'chatbot_app/prescription.html')
