from django.contrib import admin
from .models import BMIData,Trainer,personToTrainer,personToSubsc,Subscription,trainerDetails,TrainingSessions,SubscribeSessions,TrainingSessions1

admin.site.register(BMIData)
admin.site.register(Trainer)
admin.site.register(personToSubsc)
admin.site.register(personToTrainer)
admin.site.register(Subscription)
admin.site.register(trainerDetails)
admin.site.register(TrainingSessions)
admin.site.register(SubscribeSessions)
admin.site.register(TrainingSessions1)