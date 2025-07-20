from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import logging
import json

# Logger
logger = logging.getLogger(__name__)

# ✅ LOGIN
@csrf_exempt
def login_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data['userName']
        password = data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"userName": username, "status": "Authenticated"})
        else:
            return JsonResponse({"userName": username, "status": "Invalid credentials"}, status=401)
    return JsonResponse({"error": "Invalid method"}, status=400)

# ✅ LOGOUT
def logout_request(request):
    logout(request)
    return redirect('index')  # or return JsonResponse({"status": "Logged out"})

# ✅ REGISTRATION
@csrf_exempt
def registration(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data['userName']
        password = data['password']
        first_name = data.get('firstName', '')
        last_name = data.get('lastName', '')

        if User.objects.filter(username=username).exists():
            return JsonResponse({"status": "Username already exists"}, status=400)

        user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
        login(request, user)
        return JsonResponse({"userName": username, "status": "Registered and Logged in"})
    return JsonResponse({"error": "Invalid method"}, status=400)

# ✅ INDEX (Home page)
def get_dealerships(request):
    return render(request, 'Home.html')

# ✅ ABOUT
def about(request):
    return render(request, 'About.html')
