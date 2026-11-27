from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('djangoapp/', include('djangoapp.urls')),

    # Home page
    path('', TemplateView.as_view(template_name="Home.html")),

    # Login page
    path('login/', TemplateView.as_view(template_name="index.html")),

    # Registration page
    path('register/', TemplateView.as_view(template_name="index.html")),

    # Dealers page
    path('dealers/', TemplateView.as_view(template_name="index.html")),

    # Individual dealer and reviews page
    path('dealer/<int:dealer_id>', TemplateView.as_view(template_name="index.html")),

    # Post a review page
    path('postreview/<int:dealer_id>', TemplateView.as_view(template_name="index.html")),

    # About Us page
    path('about', TemplateView.as_view(template_name="About.html")),

    # Contact Us page
    path('contact', TemplateView.as_view(template_name="Contact.html")),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)