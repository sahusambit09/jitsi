from django.conf.urls import url
from django.urls import path,include
from django.views.decorators.csrf import csrf_exempt
from .  import views
urlpatterns = [
    path('conference/',csrf_exempt(views.user_status)),
    path('password/',csrf_exempt(views.check_passwordapi)),
    path('userDetails/',views.userDetails)
]