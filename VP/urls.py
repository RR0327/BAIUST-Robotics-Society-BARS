from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("panels/", views.panels_view, name="panels"),
    path("panels/<int:panel_id>/", views.panel_detail, name="panel_detail"),
    path("events/", views.events_view, name="events"),
    path("events/<int:event_id>/", views.event_detail, name="event_detail"),
    path("advisors/", views.advisors_view, name="advisors"),
    path("advisors/<int:advisor_id>/", views.advisor_detail, name="advisor_detail"),
    path("members/", views.members_view, name="members"),  # Add this line
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.user_profile, name="user_profile"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("export-members/", views.export_members_csv, name="export_members_csv"),
    # Password reset urls (using Django's built-in auth views)
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="VP/password_reset.html",
            email_template_name="VP/password_reset_email.html",  # Used as fallback/text
            subject_template_name="VP/password_reset_subject.txt",
            html_email_template_name="VP/password_reset_email.html",  # CRITICAL: Send as HTML
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="VP/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="VP/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="VP/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
