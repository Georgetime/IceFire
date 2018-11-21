# -*- coding:utf-8 -*-

# from .forms import LoginForm
from django.contrib import auth
from django.shortcuts import render, HttpResponseRedirect
# from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# def acc_login(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = auth.authenticate(username=username, password=password)
#             if user is not None and user.is_active:
#                 auth.login(request, user)
#                 request.session['user_id'] = user.id
#                 # return render(request, 'index.html', {'user': username})
#                 return HttpResponseRedirect(reverse('dashboard'))
#             else:
#                 message = "Wrong Username or Password, Try again!"
#                 return render(request, 'login.html', {'form': form,
#                                                       'message': message})
#     else:
#         form = LoginForm()
#         print(form)
#     return render(request, "login.html", {'form': form})


def acc_login(request):
    if request.method == "POST":

        username = request.POST.get('email')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if user.valid_end_time: #设置了end time
                if timezone.now()  >  user.valid_begin_time and timezone.now()  <  user.valid_end_time:
                    auth.login(request, user)
                    request.session.set_expiry(60*30)
                    #print 'session expires at :',request.session.get_expiry_date()
                    return HttpResponseRedirect('/')
                else:
                    return render(request, 'login.html',
                                  {'message': 'User account is expired,please contact your IT guy for this!'})
            elif timezone.now() > user.valid_begin_time:
                    auth.login(request, user)
                    request.session.set_expiry(60*30)
                    return HttpResponseRedirect('/')

        else:
            return render(request, 'login.html', {'message': "Wrong Username or Password, Try again!"})
    else:
        return render(request, 'login.html')


@login_required
def logout(request):
    auth.logout(request)
    return render(request, 'login.html')


@login_required
def index(request):

    return render(request, 'index.html')
