from knox.views import LogoutView

from django.urls import path

from . import views

urlpatterns = [
    path('sign-up/', views.register_generic_view),
    path('log-in/', views.login_generic_view),
    path('log-out/', LogoutView.as_view()),
]