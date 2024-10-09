"""
URL configuration for GymSite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from main.views import subscribeSession,add_training_session,home,deleteSession1,contactUs,loginPage,signUp,getTrainerDetails,logoutPage,userpanel,change_bmi,getBMI,subscribeTrainer,showSubscriptions,trainerSignuo,trainerUpdate,AddTrainerDetails,addCertification,deleteSession
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('about/', contactUs),path('login/', loginPage),path('signup/', signUp),path('logout/', logoutPage),
    path('userpanel/', userpanel),path('changeBMI/', change_bmi, name='change_bmi'),path('getBMI/', getBMI, name='getBMI'),path('subscribeTrainer/<id>', subscribeTrainer, name='subscribeTrainer'),
path('showSubscriptions/<id>/', showSubscriptions),
path('trainersignup/', trainerSignuo),
path('updateTrainer/', trainerUpdate),
path('trainerUpdate/', AddTrainerDetails),
path('addCertification/', addCertification),
path('deleteSession/<id>/', deleteSession),
path('getTrainerDetails/<id>/', getTrainerDetails),
path('add_training_session/', add_training_session),
path('subscribeSession/<id>', subscribeSession),
path('deleteSession1/<id>', deleteSession1),

]
