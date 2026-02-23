import csv
from datetime import datetime, timedelta
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q, Count
from django.db.models.functions import TruncMonth

from .models import Panel, Member, Advisor, Event, UserProfile
from .forms import RegistrationForm, UserUpdateForm, UserProfileForm

# --- Helper Functions ---


def is_admin(user):
    """Helper to check if the user is authorized as admin."""
    try:
        return user.userprofile.user_type == "admin"
    except:
        return False


# --- Public Views ---


def index(request):
    """Landing page with panel info and upcoming events."""
    panels = Panel.objects.all().order_by("-year")
    upcoming_events = Event.objects.filter(status__in=["Upcoming", "Ongoing"]).order_by(
        "date"
    )[:3]
    completed_events = Event.objects.filter(status="Completed").order_by("-date")[:3]

    context = {
        "panels": panels,
        "upcoming_events": upcoming_events,
        "completed_events": completed_events,
    }
    return render(request, "index.html", context)


def panels_view(request):
    """View for displaying all panels."""
    return render(request, "VP/panels.html", {"panels": Panel.objects.all()})


def panel_detail(request, panel_id):
    """Detailed view for a specific panel roster."""
    panel = get_object_or_404(Panel, id=panel_id)
    return render(
        request,
        "VP/panel_detail.html",
        {"panel": panel, "members": panel.members.all().order_by("order")},
    )


def events_view(request):
    """Refined search and filtering logic."""
    status_filter = request.GET.get("status", "all")
    search_query = request.GET.get("search", "")

    # Base queryset
    events = Event.objects.all().order_by("-date")

    # Refined Search: Title, Location, and Description
    if search_query:
        events = events.filter(
            Q(title__icontains=search_query)
            | Q(location__icontains=search_query)
            | Q(description__icontains=search_query)
        )

    if status_filter != "all":
        events = events.filter(status=status_filter)

    context = {
        "events": events,
        "search_query": search_query,
        "status_filter": status_filter,
    }
    return render(request, "VP/events.html", context)


def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, "VP/event_detail.html", {"event": event})


def event_photos(request, event_id):
    """Gallery view for a specific mission/event."""
    event = get_object_or_404(Event, id=event_id)
    photos = event.photos.all()
    return render(
        request,
        "VP/event_photos.html",
        {"event": event, "photos": photos},
    )


def event_results(request, event_id):
    """Winner standings for a specific mission/event."""
    event = get_object_or_404(Event, id=event_id)
    results = event.results.all()
    
    # Separate champion and runner-up from other results
    champion = results.filter(rank="Champion").first()
    runner_up_1 = results.filter(rank="1st Runner-up").first()
    other_results = results.exclude(rank__in=["Champion", "1st Runner-up"])
    
    return render(
        request,
        "VP/event_results.html",
        {
            "event": event,
            "champion": champion,
            "runner_up_1": runner_up_1,
            "other_results": other_results,
        },
    )


def advisors_view(request):
    """View for faculty advisors."""
    return render(request, "VP/advisors.html", {"advisors": Advisor.objects.all()})


def advisor_detail(request, advisor_id):
    """Detailed view for a specific faculty advisor."""
    advisor = get_object_or_404(Advisor, id=advisor_id)
    return render(request, "VP/advisor_detail.html", {"advisor": advisor})


def members_view(request):
    """Filterable directory of all society members."""
    members = Member.objects.all().select_related("panel")
    selected_panel = request.GET.get("panel", "all")
    selected_role = request.GET.get("role", "all")

    if selected_panel != "all":
        members = members.filter(panel_id=selected_panel)
    if selected_role != "all":
        members = members.filter(role=selected_role)

    context = {
        "members": members,
        "panels": Panel.objects.all(),
        "selected_panel": selected_panel,
        "selected_role": selected_role,
    }
    return render(request, "VP/members.html", context)


# --- Authentication Views ---


def register_view(request):
    """Handles new user registration and profile initialization."""
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
    """Handles terminal access for authorized users."""
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            if is_admin(user):
                return redirect("admin_dashboard")
            return redirect("index")
    else:
        form = AuthenticationForm()
    return render(request, "VP/login.html", {"form": form})


def logout_view(request):
    """Terminates session and clears local data."""
    auth_logout(request)
    messages.success(request, "LOGOUT SUCCESSFUL. SESSION TERMINATED.")
    return redirect("index")


@login_required
def user_profile(request):
    """User management console for personal data updates."""
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


# --- Administrative Terminal Views ---


@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    """
    Administrative Command Deck.
    Includes Growth Analytics, Operational Timers, and System Logs.
    """
    panels = Panel.objects.all().order_by("-year")
    members = Member.objects.all()
    events = Event.objects.all()

    # 1. Growth Chart Analytics (Last 6 Months)
    six_months_ago = datetime.now() - timedelta(days=180)
    growth_data = (
        UserProfile.objects.filter(created_at__gte=six_months_ago)
        .annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(total=Count("id"))
        .order_by("month")
    )

    chart_labels = [d["month"].strftime("%b %Y") for d in growth_data]
    chart_values = [d["total"] for d in growth_data]

    # 2. Operational Awareness
    upcoming_schedule = events.filter(status="Upcoming").order_by("date")

    context = {
        "panels": panels,
        "total_members": members.count(),
        "total_events": events.count(),
        "upcoming_ops": upcoming_schedule.count(),
        "active_panel": panels.first() if panels.exists() else None,
        "recent_registrations": members.order_by("-id")[:5],
        "upcoming_schedule": upcoming_schedule[:5],
        "chart_labels": chart_labels,
        "chart_values": chart_values,
    }
    return render(request, "VP/admin_dashboard.html", context)


@login_required
@user_passes_test(is_admin)
def export_members_csv(request):
    """Generates a CSV report of society roster for official use."""
    response = HttpResponse(content_type="text/csv")
    filename = f"BARS_Roster_{datetime.now().strftime('%Y-%m-%d')}.csv"
    response["Content-Disposition"] = f'attachment; filename="{filename}"'

    writer = csv.writer(response)
    writer.writerow(["FULL NAME", "DESIGNATION", "PANEL YEAR", "CONTACT EMAIL"])

    members = Member.objects.all().select_related("panel")
    for m in members:
        writer.writerow([m.name, m.role, m.panel.year, m.email])

    return response
