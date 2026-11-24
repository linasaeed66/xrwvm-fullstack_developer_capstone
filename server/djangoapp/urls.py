
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'

urlpatterns = [
    # Login route
    path(route='login', view=views.login_user, name='login'),

    # Logout route
    path(route='logout', view=views.logout_request, name='logout'),

    # Registration route
    path(route='register', view=views.registration, name='register'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
