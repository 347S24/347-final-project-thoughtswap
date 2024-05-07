from django.urls import path

from .views import SignUpView
from discussion.views import register_facilitator


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path('register/', register_facilitator, name='register-facilitator'),
    # path('signup/', register_facilitator, name='register-facilitator'),
]