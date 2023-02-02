from knox.views import LogoutView

from django.urls import path

from . import views

urlpatterns = [
    path('sign-up/', views.register_generic_view, name='sign-up'),
    path('log-in/', views.login_generic_view, name='login'),
    path('log-out/', LogoutView.as_view(), name='logout'),
]