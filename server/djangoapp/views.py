
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create a login view to handle sign in request
@csrf_exempt
def login_user(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']

    user = authenticate(username=username, password=password)
    data = {"userName": username}

    if user is not None:
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}

    return JsonResponse(data)


# Create a logout view to handle sign out request
def logout_request(request):
    logout(request)
    data = {"userName": ""}
    return JsonResponse(data)


# Create a registration view to handle sign up request
@csrf_exempt
def registration(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        username = data.get('userName', '').strip()
        password = data.get('password', '')
        first_name = data.get('firstName', '').strip()
        last_name = data.get('lastName', '').strip()
        email = data.get('email', '').strip()

        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Already Registered"})

        if not username or not password:
            return JsonResponse({"error": "Username and password are required"})

        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email
        )

        login(request, user)

        return JsonResponse({
            "userName": username,
            "status": True
        })

    return JsonResponse({"error": "Invalid request method"})


# Update the get_dealerships view
# def get_dealerships(request):
# ...


# Create a get_dealer_reviews view
# def get_dealer_reviews(request, dealer_id):
# ...


# Create a get_dealer_details view
# def get_dealer_details(request, dealer_id):
# ...


# Create an add_review view
# def add_review(request):
# ...
