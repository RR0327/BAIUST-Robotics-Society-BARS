from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from .models import Panel, Member, Advisor, Event, UserProfile
from .forms import RegistrationForm, UserUpdateForm, UserProfileForm


def index(request):
    panels = Panel.objects.all().order_by("-year")
    upcoming_events = Event.objects.filter(status__in=["Upcoming", "Ongoing"]).order_by(
        "date"
    )[:3]
    completed_events = Event.objects.filter(status="Completed").order_by("-date")[:3]
    return render(
        request,
        "index.html",
        {
            "panels": panels,
            "upcoming_events": upcoming_events,
            "completed_events": completed_events,
        },
    )


def panels_view(request):
    return render(request, "VP/panels.html", {"panels": Panel.objects.all()})


def panel_detail(request, panel_id):
    panel = get_object_or_404(Panel, id=panel_id)
    return render(
        request,
        "VP/panel_detail.html",
        {"panel": panel, "members": panel.members.all().order_by("order")},
    )


def events_view(request):
    status_filter = request.GET.get("status", "all")
    search_query = request.GET.get("search", "")

    events = Event.objects.all()

    # Apply status filter
    if status_filter != "all":
        events = events.filter(status=status_filter)

    # Apply search filter
    if search_query:
        events = events.filter(
            Q(title__icontains=search_query)
            | Q(description__icontains=search_query)
            | Q(location__icontains=search_query)
        )

    # Count events by status
    upcoming_count = Event.objects.filter(status="Upcoming").count()
    ongoing_count = Event.objects.filter(status="Ongoing").count()
    completed_count = Event.objects.filter(status="Completed").count()

    context = {
        "events": events,
        "status_filter": status_filter,
        "search_query": search_query,
        "upcoming_count": upcoming_count,
        "ongoing_count": ongoing_count,
        "completed_count": completed_count,
    }
    return render(request, "VP/events.html", context)


def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, "VP/event_detail.html", {"event": event})


def advisors_view(request):
    advisors = Advisor.objects.all()
    return render(request, "VP/advisors.html", {"advisors": advisors})


# Advisor detail view
def advisor_detail(request, advisor_id):
    advisor = get_object_or_404(Advisor, id=advisor_id)
    return render(request, "VP/advisor_detail.html", {"advisor": advisor})


def register_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(
                user=user,
                user_type=form.cleaned_data.get("user_type", "student"),
                student_id=form.cleaned_data.get("student_id", ""),
                phone=form.cleaned_data.get("phone", ""),
            )
            login(request, user)
            messages.success(request, "Registration successful! Welcome to BARS.")
            return redirect("index")
    else:
        form = RegistrationForm()
    return render(request, "VP/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            try:
                if user.userprofile.user_type == "admin":
                    return redirect("admin_dashboard")
            except UserProfile.DoesNotExist:
                pass
            return redirect("index")
    else:
        form = AuthenticationForm()
    return render(request, "VP/login.html", {"form": form})


def logout_view(request):
    """
    Handles user logout, flushes session data,
    and redirects to the landing page.
    """
    auth_logout(request)
    messages.success(request, "LOGOUT SUCCESSFUL. SESSION TERMINATED.")
    return redirect("index")


def is_admin(user):
    try:
        return user.userprofile.user_type == "admin"
    except:
        return False


@login_required
@user_passes_test(
    lambda u: hasattr(u, "userprofile") and u.userprofile.user_type == "admin"
)
def admin_dashboard(request):
    return render(
        request,
        "VP/admin_dashboard.html",
        {
            "panels": Panel.objects.all(),
            "events": Event.objects.all(),
            "members": Member.objects.all(),
        },
    )


@login_required
def user_profile(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user, user_type="guest")

    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=profile)

        if form.is_valid() and profile_form.is_valid():
            form.save()
            profile_form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect("user_profile")
    else:
        form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileForm(instance=profile)

    return render(
        request, "VP/user_profile.html", {"form": form, "profile_form": profile_form}
    )


def members_view(request):
    """View for displaying all members"""
    members = Member.objects.all().select_related("panel")
    panels = Panel.objects.all()

    # Get filter parameters
    selected_panel = request.GET.get("panel", "all")
    selected_role = request.GET.get("role", "all")

    # Apply filters
    if selected_panel != "all":
        members = members.filter(panel_id=selected_panel)
    if selected_role != "all":
        members = members.filter(role=selected_role)

    context = {
        "members": members,
        "panels": panels,
        "selected_panel": selected_panel,
        "selected_role": selected_role,
    }
    return render(request, "VP/members.html", context)
