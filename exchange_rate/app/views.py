from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth import login, authenticate, logout
import os, requests
from dotenv import load_dotenv
from .models import ExchangeRateResponse
from datetime import datetime, timezone


load_dotenv()

token = os.getenv('API_TOKEN')

def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'registration/login.html', {'error_message': 'Invalid login'})
    else:
        return render(request, 'registration/login.html')


def user_logout(request):
    if not request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        logout(request)
    return render(request, 'home.html')


def get_current_usd(request):
    last_request_timestamp = ExchangeRateResponse.objects.all().order_by('-timestamp')[:1][0].timestamp  # Get last timestamp
    seconds_passed = datetime.now(timezone.utc) - last_request_timestamp
    seconds_passed = int(round(seconds_passed.total_seconds(), 0))
    context = {}

    if seconds_passed < 10:
        context.update({'seconds_passed': seconds_passed})

    else:
        url = 'https://currate.ru/api/'
        params = {
            'get': 'rates',
            'key': token,
            'pairs': 'USDRUB'
        }
        response = requests.get(url, params).json()['data']
        ExchangeRateResponse.objects.create(user=request.user, response=response)
    user_responses = ExchangeRateResponse.objects.for_user(request.user).order_by('-timestamp')[:10]
    context.update({'user_responses': user_responses})

    return render(request, 'get_current_usd.html', context)
