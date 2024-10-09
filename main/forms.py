from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import trainerDetails,Trainer,TrainingSessions,TrainingSessions1
from django.forms import TimeInput
class CreateUserform(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name']

class CreateTrainerForm(UserCreationForm):
    is_staff = forms.BooleanField(initial=True, widget=forms.HiddenInput)
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name' ,'is_staff']
    def __init__(self, *args, **kwargs):
        super(CreateTrainerForm, self).__init__(*args, **kwargs)
        self.fields['is_staff'].initial = True

class updateTrainer(ModelForm):
    class Meta:
        model = trainerDetails
        fields = ['course','certification']

class CreateTrainer(forms.ModelForm):
    class Meta:
        model = Trainer
        fields = ['name','field','comments','profile_pic']
class trainingSessions(forms.ModelForm):
    class Meta:
        model = Trainer
        fields = ['name','field','comments','profile_pic']

class TrainingSessionsForm(forms.ModelForm):
    class Meta:
        model = TrainingSessions
        fields = ['Sessions']

class TrainingSessionsForm1(forms.ModelForm):
    class Meta:
        model = TrainingSessions1
        fields = ['sessions', 'start_time', 'end_time']
        widgets = {
            'start_time': TimeInput(attrs={'type': 'time'}),
            'end_time': TimeInput(attrs={'type': 'time'}),
        }

