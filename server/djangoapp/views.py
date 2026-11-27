
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_exempt
from .models import CarMake, CarModel
from .populate import initiate
from .restapis import get_request, analyze_review_sentiments, post_review
import logging
import json

logger = logging.getLogger(__name__)


# Login view
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


# Logout view
def logout_request(request):
    logout(request)
    data = {"userName": ""}
    return JsonResponse(data)


# Registration view
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
            return JsonResponse({
                "error": "Username and password are required"
            })

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


# Get all car makes and models
def get_cars(request):
    count = CarMake.objects.count()

    if count == 0:
        initiate()

    car_models = CarModel.objects.select_related('car_make')
    cars = []

    for car_model in car_models:
        cars.append({
            "CarModel": car_model.name,
            "CarMake": car_model.car_make.name
        })

    return JsonResponse({"CarModels": cars})


# Get all dealerships or dealerships filtered by state
def get_dealerships(request, state="All"):
    if state == "All":
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/" + state

    dealerships = get_request(endpoint)

    return JsonResponse({
        "status": 200,
        "dealers": dealerships
    })


# Get details for a specific dealership
def get_dealer_details(request, dealer_id):
    endpoint = "/fetchDealer/" + str(dealer_id)
    dealership = get_request(endpoint)

    return JsonResponse({
        "status": 200,
        "dealer": dealership
    })


# Get reviews for a dealership and analyse their sentiments
def get_dealer_reviews(request, dealer_id):
    endpoint = "/fetchReviews/dealer/" + str(dealer_id)
    reviews = get_request(endpoint)

    for review in reviews:
        sentiment = analyze_review_sentiments(review["review"])
        review["sentiment"] = sentiment["sentiment"]

    return JsonResponse({
        "status": 200,
        "reviews": reviews
    })


# Add a review (authenticated users only)
@csrf_exempt
def add_review(request):
    if not request.user.is_authenticated:
        return JsonResponse(
            {"error": "Authentication required"},
            status=403
        )

    if request.method != "POST":
        return JsonResponse(
            {"error": "Invalid request method"},
            status=405
        )

    try:
        data = json.loads(request.body)
        post_review(data)

        return JsonResponse({"status": 200})

    except (json.JSONDecodeError, KeyError, ValueError) as error:
        logger.error("Unable to add review: %s", error)
        return JsonResponse(
            {"error": "Invalid review data"},
            status=400
        )
