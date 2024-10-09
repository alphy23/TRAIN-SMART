from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse,HttpResponseBadRequest
from django.forms import inlineformset_factory
from .forms import CreateUserform,CreateTrainerForm,updateTrainer,CreateTrainer,TrainingSessionsForm,TrainingSessionsForm1
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import BMIData,Trainer,personToTrainer,Subscription,personToSubsc,trainerDetails,TrainingSessions,SubscribeSessions,TrainingSessions1
from django.contrib.auth import authenticate, login,logout

import json

# views.py

from django.http import JsonResponse

from .test import send_email

def showSubscriptions(request,id):
    data =Subscription.objects.filter(id=id)
    print(data)
    try:
        single_object = personToSubsc.objects.get(user=request.user.id,subscription = id)
        print(single_object)
        
        single_object.delete()
        
    except personToSubsc.DoesNotExist:
        insc = personToSubsc(user=request.user,subscription = data[0])
        insc.save()
        print("No Value Found")
        
    # print(id)
    return redirect("/userpanel/")

def subscribeTrainer(request,id):
    data =Trainer.objects.filter(id=id)
    print(data)
    try:
        single_object = personToTrainer.objects.get(user=request.user.id,trainer = data[0])
        single_object.delete()
        # print(single_object)
        
    except personToTrainer.DoesNotExist:
        insc = personToTrainer(user=request.user,trainer = data[0])
        insc.save()
        # print("saved")
    return redirect('/userpanel/')
    return HttpResponse(True)

    # return JsonResponse({'error': 'Object does not exist'}, status=404)

def getBMI(request):
    
    try:
        single_object = BMIData.objects.get(userID=request.user.id)
        data = {
                'age': single_object.age,
                'height': single_object.height,
                'weight': single_object.weight,
                'BMI': single_object.BMI,
            }

        return JsonResponse(data)
    except BMIData.DoesNotExist:
        data = {
                'age': "",
                'height': "",
                'weight': "",
                'BMI': "",
            }

        return JsonResponse(data)
        # return JsonResponse({'error': 'Object does not exist'}, status=404)



def change_bmi(request):

    if request.method == 'POST':
        decoded_string = request.body.decode("utf-8")

        json_object = json.loads(decoded_string)
        # Get the data from the POST request
        age = json_object['age']
        height = json_object['height']
        weight = json_object['weight']
        # bmi = json_object['BMI']
        print(height)
        new_height = height/100
        # Perform the BMI calculation and update the model here
        bmi = weight / ((new_height)** 2)
        print(bmi)
        # print(type(request.user.id))
        try:
            single_object = BMIData.objects.get(userID=request.user.id)
        except BMIData.DoesNotExist:
            single_object = False
        if single_object:
            print("Object Exists")
            BMIData.objects.filter(userID=request.user.id).update(userID=request.user.id,age=age,height=height,weight=weight,BMI=bmi)
            print("Updated")
            print(age,height,weight,bmi)
        else:
            insc = BMIData(userID=request.user.id,age=age,height=height,weight=weight,BMI=bmi)
            insc.save()

        print(bmi,height,weight)
        # Update your model with the calculated BMI
        # YourModel.objects.filter(your_conditions).update(bmi_field=bmi)

        # Respond with a success message or updated data
        return JsonResponse({'message': 'BMI updated successfully', 'bmi': bmi})
    else:
        return JsonResponse({'message': 'Invalid request'})




@login_required(login_url="/login")
def userpanel(request):
    isSubscribed = False
    
    trainers = Subscription.objects.all()
    trainers_subs = personToSubsc.objects.filter(user=request.user.id)
    # print(trainers)
    # for j in trainers:
    #     print(j.id)
    data = {}
    for i in trainers:
        # print("Subscription name")
        # print(i.name)
        services = i.services.split(',')
        # print(services)
        for j in trainers_subs:
            # print(j.subscription.id)
            if j.subscription.id ==i.id:
                isSubscribed = True
            else:
                isSubscribed = False
                
        data[i.id] = {"name":i.name,"pricing":i.pricing,"services":services,"subscribed":isSubscribed}
    context = {}
    # print(data)
    trainers = Trainer.objects.all()
    
    
    for i in trainers:
        subscribed = personToTrainer.objects.filter(user=request.user.id,trainer = i.id)
        # print(subscribed.count())
        
        # if i.id in subscribed:
        #     subs= True
        # else:
        #     subs= False
        # print(subs)
        if subscribed.count() == 1:
            trainer = {"id":i.id,"name":i.name,"field":i.field,"comments":i.comments,"image":i.profile_pic.url,"subscribed":True }
        else:
            trainer = {"id":i.id,"name":i.name,"field":i.field,"comments":i.comments,"image":i.profile_pic.url,"subscribed":False }
            
        context[i.id] = trainer
    # print(context)
    return render(request,'userpanel.html',{'my_context': context,"subs":data})

# Create your views here.
def home(request):
    # print(request.user.id)
    trainer = []
    trainers = Trainer.objects.all()
    for i in trainers:
        
        trainer.append( {"id":i.id,"name":i.name,"field":i.field,"comments":i.comments,"image":i.profile_pic.url,"subscribed":True })
        
    return render(request,'home.html',{"trainer":trainer})

def contactUs(request):
    trainer = []
    trainers = Trainer.objects.all()
    for i in trainers:
        
        trainer.append( {"id":i.id,"name":i.name,"field":i.field,"comments":i.comments,"image":i.profile_pic.url,"subscribed":True })
       
    if request.method =="POST":
        # print(request.POST)
        # print(request.POST["email"])
        # print(request.POST["subject"])
        # print(request.POST["message"])
        send_email("Gym Site Contact | "+request.POST["subject"],request.POST["message"],["saeil.moorsingal@gmail.com",request.POST["email"]])
    return render(request,'contact.html',{"trainer":trainer})

def loginPage(request):

    context = {}
    
    if request.method =='POST':
        context = {"name":request.POST["email"]}
        print(type(request.POST))
        print(request.POST["email"])
        print(request.POST["password"])
        user = authenticate(request, username =request.POST["email"],password =request.POST["password"]  )
        print(user)
        if user is not None:
            login(request,user)
            return redirect('/')
        else:
            messages.success(request,"Login Failed. Username or password is incorect")

        
    return render(request,'login.html',context)


def logoutPage(request):
    logout(request)
    return redirect('/login')


def signUp(request):
    form = CreateUserform()
    context = {'form': form}
    if request.method == 'POST':
        form = CreateUserform(request.POST)
        print("Post Methord")
        print("Checking If valid or not")
        print(form.is_valid())
        if form.is_valid():
            print("Saving Form")
            
            form.save()
            username = form.cleaned_data.get('username')
            print(username)
            messages.success(request,"Account created for username "+username)
            return redirect("/login")
        else:
            context['form'] = form
    return render(request,'signup.html',context)

def trainerSignuo(request):
    form = CreateTrainerForm()
    context = {'form': form}
    if request.method == 'POST':
        form = CreateTrainerForm(request.POST)
        print("Post Methord")
        print("Checking If valid or not")
        print(form.is_valid())
        if form.is_valid():
            print("Saving Form")
            
            form.save()
            username = form.cleaned_data.get('username')
            print(username)
            messages.success(request,"Account created for username "+username)
            return redirect("/trainerUpdate/")
        else:
            context['form'] = form
    return render(request,'signup.html',context)


def AddTrainerDetails(request):
    data =Trainer.objects.filter(user=request.user.id)
    trainer_details = trainerDetails.objects.filter(user=request.user.id)
    Session_Details = TrainingSessions1.objects.filter(user=request.user.id)
    session_details = []
    print(Session_Details)
    print(len(trainer_details))
    if len(data)==0:
        return redirect("/updateTrainer/")
    else:
        trainer = []
        for i in data:
            trainer.append( {"id":i.id,"name":i.name,"field":i.field,"comments":i.comments,"image":i.profile_pic.url,"subscribed":True })

    for i in Session_Details:
        print(i)
        print("Finding Details")
        try:
            single_object = SubscribeSessions.objects.get(Sessions=i)
            print(single_object.user)
            session_details.append({"id":i.id,"sessions":i.sessions,"start_time":i.start_time,"end_time":i.end_time,"user":single_object.user})
        except SubscribeSessions.DoesNotExist:
            session_details.append({"id":i.id,"sessions":i.sessions,"start_time":i.start_time,"end_time":i.end_time,"user":""})

        
    return render(request,"trainerpanel.html",{'trainer':trainer,"sessions":trainer_details,"training_sessions":session_details})

@login_required(login_url="/login")
def trainerUpdate(request):
    form = CreateTrainer()
    # print(form)
 
    if request.method == 'POST':
        # print(request.POST, request.FILES)
        form = CreateTrainer(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
        return redirect("/trainerUpdate/")

    return render(request,'update_trainer.html',{'form': form})

def addCertification(request):
    form = updateTrainer()
    # print(form)
    if request.method == 'POST':
        form = updateTrainer(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
        return redirect("/trainerUpdate/")

    return render(request,'update_trainer.html',{'form': form})


def deleteSession(request,id):
    
    single_object = trainerDetails.objects.get(id=id)
    print(single_object)
    single_object.delete()
    print(id)
        
    return redirect("/trainerUpdate/")

def getTrainerDetails(request,id):
    # print(id)
    data =Trainer.objects.filter(id = id)
    trainers = Subscription.objects.all()
    training_sessions = TrainingSessions.objects.all()
    training_sessions = TrainingSessions1.objects.all()
    # print(training_sessions)
    trainer_details = trainerDetails.objects.filter(user = id)
    trainer_details = trainerDetails.objects.all()
    trainingSessions = SubscribeSessions.objects.filter(user = request.user.id)
    trainingSessions = SubscribeSessions.objects.all()
    print(trainingSessions)
    
    # print("training Session : "+str(trainingSessions[0].Sessions))
    extra = []
    tr_sessions = []
    bSubsctribedFlag = False

    context = {}
    for i in data:
        trainer_user_id = i.user.id
        subscribed = personToTrainer.objects.filter(user=request.user.id,trainer = i.id)
        if subscribed.count() == 1:
            trainer = {"id":i.id,"name":i.name,"field":i.field,"comments":i.comments,"image":i.profile_pic.url,"subscribed":True }
        else:
            trainer = {"id":i.id,"name":i.name,"field":i.field,"comments":i.comments,"image":i.profile_pic.url,"subscribed":False }
            
        context[i.id] = trainer
    # for i in training_sessions:
    #     bSubsctribedFlag = False

    #     for j in trainingSessions:
    #         # print(str(i) ==str(j))
    #         if str(i) ==str(j.Sessions):
    #             bSubsctribedFlag = True
    #             break
    #     if int(i.user.id)==int(trainer_user_id):
    #         print({"id":i.id,"Sessions":i.Sessions,"status":bSubsctribedFlag})
    for i in training_sessions:
        bSubsctribedFlag = False
        bSomeoneElse = False

        for j in trainingSessions:
            # print(str(i) ==str(j))
            print(j.user.id !=request.user.id)
            if str(i) ==str(j.Sessions) and j.user.id ==request.user.id:
                bSubsctribedFlag = True
                break
            if str(i) ==str(j.Sessions) and j.user.id !=request.user.id:
                bSomeoneElse = True
        # if bSomeoneElse:
        #     tr_sessions.append({"bSomeoneElse":bSomeoneElse,"id":i.id,"Sessions":i.sessions,"start_time":i.start_time,"end_time":i.end_time,"status":bSubsctribedFlag})
        if int(i.user.id)==int(trainer_user_id):
            print({"id":i.id,"Sessions":i.sessions,"start_time":i.start_time,"end_time":i.end_time,"status":bSubsctribedFlag})
            tr_sessions.append({"bSomeoneElse":bSomeoneElse,"id":i.id,"Sessions":i.sessions,"start_time":i.start_time,"end_time":i.end_time,"status":bSubsctribedFlag})
        print(tr_sessions)
    for i in trainer_details:
        if int(i.user.id)==int(trainer_user_id):
            extra.append(i)
    return render(request,'trainerDetails.html',{"trainer":trainer,"sessions":extra,'training':tr_sessions})


def add_training_session(request):
# Check if the user is authenticated
    if not request.user.is_authenticated:
        # Redirect to a login page or show an error message
        return redirect('login')

    if request.method == 'POST':
        form = TrainingSessionsForm1(request.POST)
        if form.is_valid():
            # Save the form with the current user
            session = form.save(commit=False)
            session.user = request.user
            session.save()
            return redirect('/trainerUpdate/')  # Redirect to a success page or any other view
    else:
        form = TrainingSessionsForm1()

    return render(request, 'add_training_session.html', {'form': form})


def subscribeSession(request,id):
    data =TrainingSessions.objects.filter(id=id)
    data =TrainingSessions1.objects.filter(id=id)
    print(data[0])

    try:
        single_object = SubscribeSessions.objects.get(user=request.user,Sessions = data[0])
        single_object.delete()
        # print(single_object)
        
    except SubscribeSessions.DoesNotExist:
        insc = SubscribeSessions(user=request.user,Sessions = data[0])
        insc.save()
    return redirect("/userpanel")


def deleteSession1(request,id):
    print(id)
    single_object = TrainingSessions1.objects.get(id=id)
    print(single_object)
    single_object.delete()
    return redirect("/trainerUpdate")


