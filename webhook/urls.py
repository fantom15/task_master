from django.urls import path
from .views import send_template_message,webhook

urlpatterns = [
    path("api/send/", send_template_message),
    path('webhook/', webhook, name='webhook'),
]
