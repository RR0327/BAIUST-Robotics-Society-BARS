# VP/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("panels/", views.panels_view, name="panels"),
    path("panels/<int:panel_id>/", views.panel_detail, name="panel_detail"),
    path("events/", views.events_view, name="events"),
    path("advisors/", views.advisors_view, name="advisors"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
]
