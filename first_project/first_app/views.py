from django.shortcuts import render
from first_app.models import Topic, WebPage, AccessRecord
from django.http import HttpResponse
from . import forms
from first_app.forms import UserForm, UserProfileInfoForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

# Create your views here.

def index(request):
    webpages_list = AccessRecord.objects.order_by('date')
    my_type = type(webpages_list)
    date_dict = {'access_records': webpages_list, 'my_name': "jay", "my_type": my_type}
    return render(request, 'first_app/index.html', context = date_dict)

def form_name_view(request):
    form = forms.FormName()

    if request.method == "POST":
        form = forms.FormName(request.POST)
        if form.is_valid():
            # do something code
            print(form.cleaned_data['name'])
            print(form.cleaned_data['email'])
            print(form.cleaned_data['text'])



    return render(request, 'first_app/form_page.html', {'form' : form})

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form  = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user # OneToOneField

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'first_app/registration.html',
                                {'registered':registered,
                                'user_form':user_form,
                                'profile_form':profile_form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("ACCOUNT NOT ACTIVATE")
        else:
            print("Someone tried to login and failed")
            print(f"username: {username} and password {password}")
            logged_in = "Invalid Login Details"
            return render(request, 'first_app/login.html', {'logged_in' : logged_in})
            #return HttpResponse("Invalid Login Details")

    else:
        return render(request, 'first_app/login.html', {})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required
def special(request):
    return HttpResponse("You Are Logged In, Nice")
