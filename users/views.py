from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    valuenext =  request.POST.get('next')
    if request.method == 'POST':

        usrname = request.POST['username']
        passwd = request.POST['password']

        user = authenticate(request, username=usrname, password=passwd)  # None
        if user is not None and valuenext=='':
            login(request, user)
            context= {
                      'valuenext': valuenext}
            return redirect('home')
        elif user is not None and valuenext !='':
        	login(request, user)
        	context = {
        	'valuenext': valuenext}
        	return redirect(valuenext)
        else:
            messages.warning(
                request, f'Please enter a correct username and password. Note that both fields may be case-sensitive.')
            return redirect('login')

    form = AuthenticationForm()
    return render(request, 'user/login.html', {'form': form})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(
                request, 'Your password was successfully updated!')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'home/changePassword.html', {
        'form': form,

    })