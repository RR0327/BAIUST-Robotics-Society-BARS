from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import Panel, Member, Advisor, Event, UserProfile
from .forms import RegistrationForm


def index(request):
    panels = Panel.objects.all()
    upcoming_events = Event.objects.filter(status__in=["Upcoming", "Ongoing"])[:3]
    completed_events = Event.objects.filter(status="Completed")[:3]

    context = {
        "panels": panels,
        "upcoming_events": upcoming_events,
        "completed_events": completed_events,
    }
    return render(request, "index.html", context)


def panels_view(request):
    panels = Panel.objects.all()
    return render(request, "VP/panels.html", {"panels": panels})


def panel_detail(request, panel_id):
    panel = get_object_or_404(Panel, id=panel_id)
    members = panel.members.all()
    return render(request, "VP/panel_detail.html", {"panel": panel, "members": members})


def events_view(request):
    events = Event.objects.all()
    return render(request, "VP/events.html", {"events": events})


def advisors_view(request):
    advisors = Advisor.objects.all()
    return render(request, "VP/advisors.html", {"advisors": advisors})


def register_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_type = form.cleaned_data["user_type"]
            UserProfile.objects.create(user=user, user_type=user_type)
            messages.success(request, "Registration successful! Please login.")
            return redirect("login")
    else:
        form = RegistrationForm()
    return render(request, "VP/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect based on user type
                profile = UserProfile.objects.get(user=user)
                if profile.user_type == "admin":
                    return redirect("admin_dashboard")
                else:
                    return redirect("index")
    else:
        form = AuthenticationForm()
    return render(request, "VP/login.html", {"form": form})


def is_admin(user):
    try:
        return user.userprofile.user_type == "admin"
    except:
        return False


@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    panels = Panel.objects.all()
    events = Event.objects.all()
    members = Member.objects.all()

    context = {
        "panels": panels,
        "events": events,
        "members": members,
    }
    return render(request, "VP/admin_dashboard.html", context)
