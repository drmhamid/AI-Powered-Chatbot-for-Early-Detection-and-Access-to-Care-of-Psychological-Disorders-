from django.db import models
from authen_app.models import CustomUser
from admin_dashboard.models import doctor

# Create your models here.
class contact(models.Model):
    name = models.TextField(default='')
    email = models.TextField(default='')
    subject = models.TextField(default='')
    description = models.TextField(default='')


class profile_data(models.Model):
    CustomUser = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    f_name = models.TextField(default='')
    l_name = models.TextField(default='')
    city = models.TextField(default='')
    country = models.TextField(default='')
    gender = models.TextField(default='')
    address = models.TextField(default='')
    dob = models.DateField(null=True, blank=True)
    province = models.TextField(default='')
    image = models.TextField(default='')
    education = models.TextField(default='')
    marital_status = models.TextField(default='')
    profession = models.TextField(default='')
    age = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)


class doc_timing(models.Model):
    doctor = models.ForeignKey(doctor, on_delete=models.CASCADE)
    day = models.TextField(default='')
    timing = models.TimeField(null=True, blank=True)
    date = models.DateField(blank=True, null=True)
    status = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)


class user_appointment(models.Model):
    user_details = models.ForeignKey(profile_data, on_delete=models.CASCADE)
    doctor_details = models.ForeignKey(doctor, on_delete=models.CASCADE)
    day = models.TextField(default='')
    time = models.TimeField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)

class timing_exists(models.Model):
    doctor = models.ForeignKey(doc_timing, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

# class questions(models.Model):
#     q1 = models.TextField(default='')
#     q2 = models.TextField(default='')
#     q3 = models.TextField(default='')
#     q4 = models.TextField(default='')
#     q5 = models.TextField(default='')
#     q6 = models.TextField(default='')
#     q7 = models.TextField(default='')
#     q8 = models.TextField(default='')
#     q9 = models.TextField(default='')
#     q10 = models.TextField(default='')
#     q11 = models.TextField(default='')
#     q12 = models.TextField(default='')
#     q13 = models.TextField(default='')
#     q14 = models.TextField(default='')
#     q15 = models.TextField(default='')
#     q16 = models.TextField(default='')
#     q17 = models.TextField(default='')
#     q18 = models.TextField(default='')
#     q19 = models.TextField(default='')
#     q20 = models.TextField(default='')
#     q21 = models.TextField(default='')
#     q22 = models.TextField(default='')
#     q23 = models.TextField(default='')
#     q24 = models.TextField(default='')


class symptom_prediction(models.Model):
    user_id = models.ForeignKey(profile_data, on_delete=models.CASCADE)
    current_data = models.JSONField(default=dict, null=True, blank=True)
    # question_details = models.ForeignKey(questions, on_delete=models.CASCADE)
    insomnia = models.BooleanField(default=False)
    fatigue = models.BooleanField(default=False)
    anger = models.BooleanField(default=False)
    stomach_issues = models.BooleanField(default=False)
    suicidal_thoughts = models.BooleanField(default=False)
    lost_in_interest = models.BooleanField(default=False)
    uneasiness = models.BooleanField(default=False)
    nausea = models.BooleanField(default=False)
    dizziness = models.BooleanField(default=False)
    heart_palpitations = models.BooleanField(default=False)
    muscle_ache = models.BooleanField(default=False)
    mood_swings = models.BooleanField(default=False)
    paranoia = models.BooleanField(default=False)
    neglected_hygiene = models.BooleanField(default=False)
    erratic_behavior = models.BooleanField(default=False)
    relationship_problems = models.BooleanField(default=False)
    vivid_flashbacks = models.BooleanField(default=False)
    nightmares = models.BooleanField(default=False)
    intrusive_thoughts = models.BooleanField(default=False)
    avoidance = models.BooleanField(default=False)
    repeating_question = models.BooleanField(default=False)
    difficulty_concentrating = models.BooleanField(default=False)
    acting_impulsively = models.BooleanField(default=False)
    movement_issues = models.BooleanField(default=False)
    disorder = models.TextField(default='')


    def update_symptom_status(self):
        current_data = self.current_data
        for key, value in current_data.items():
            setattr(self, key, value)
        self.save()
