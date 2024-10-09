from django.db import models

from django.contrib.auth import get_user_model
from django.dispatch import receiver


from django.contrib.auth.models import AbstractUser
from django.db import models




# Create your models here.
class BMI(models.Model):
    userID: int
    age:int
    height:int
    weight:int
    BMI_value:int

class Subscription(models.Model):
    name = models.CharField(max_length=200,default='')
    pricing = models.CharField(max_length=200,default='')
    services = models.CharField(max_length=255)
    def __str__(self):
        return str(self.name)

class BMIData(models.Model):
    userID=models.IntegerField()
    age=models.IntegerField()
    height=models.IntegerField()
    weight=models.IntegerField()
    BMI=models.CharField(max_length=200)
    def __str__(self):
        return str(self.userID)

class Trainer(models.Model):
    user = models.ForeignKey(get_user_model(), default='',on_delete=models.CASCADE)
    name =models.CharField(max_length=200)
    field =models.CharField(max_length=200,default='')
    comments =models.CharField(max_length=200,default='')
    profile_pic = models.ImageField(upload_to ='static/img',default='')
    def __str__(self):
        return str(self.name)
    
class personToTrainer(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="user_likes")
    trainer = models.ForeignKey(Trainer,on_delete=models.CASCADE, related_name="post_likes")
    class Meta:
        unique_together = ["user", "trainer"]
    def __str__(self):
        return str(self.id)
class personToSubsc(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="subPerson")
    subscription = models.ForeignKey(Subscription,on_delete=models.CASCADE, related_name="subSub")

class trainerDetails(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    course = models.CharField(max_length=200,default='')
    certification = models.CharField(max_length=200,default='')
    def __str__(self):
        return str(self.id)
        
class TrainingSessions(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    Sessions = models.CharField(max_length=200,default='')
    
    def __str__(self):
        return str(self.id)



from datetime import datetime, timedelta

class TrainingSessions1(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    sessions = models.CharField(max_length=200, default='')
    start_time = models.TimeField()
    end_time = models.TimeField()
    

    def save(self, *args, **kwargs):
        # Create datetime objects from the start time and end time
        start_datetime = datetime.combine(datetime.today(), self.start_time)
        end_datetime = datetime.combine(datetime.today(), self.end_time)
        print(end_datetime)
        
        # If the end time is smaller than the start time, change the date to the next day
        if end_datetime < start_datetime:
            end_datetime = end_datetime.replace(day=end_datetime.day + 1)
        # Calculate the time difference in minutes
        time_diff = (end_datetime - start_datetime).total_seconds() // 60
        # If the difference is greater than 60 minutes, split the session
        if time_diff > 60:
            # Calculate the number of records to create
            num_records = time_diff // 60
            # Loop through the number of records
            for i in range(int(num_records)):
                # Create a new record with the same user and sessions
                new_record = TrainingSessions1(user=self.user, sessions=self.sessions)
                # Set the start time to the original start time plus i hours
                new_record.start_time = (start_datetime + timedelta(hours=i)).time()
                # Set the end time to the start time plus one hour
                new_record.end_time = (start_datetime + timedelta(hours=i+1)).time()
                # Save the new record
                new_record.save()
        else:
            # If the difference is less than or equal to 60 minutes, save the original record
            super().save(*args, **kwargs)





class SubscribeSessions(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    Sessions = models.ForeignKey(TrainingSessions1, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.id)
    
