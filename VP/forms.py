from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Panel, Member, Event, Advisor


class RegistrationForm(UserCreationForm):
    USER_TYPES = [
        ("student", "Student"),
        ("guest", "Guest"),
    ]

    user_type = forms.ChoiceField(choices=USER_TYPES)
    email = forms.EmailField(required=True)
    student_id = forms.CharField(required=False, max_length=50)
    phone = forms.CharField(required=False, max_length=20)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "user_type"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = [
            "panel",
            "name",
            "role",
            "photo",
            "bio",
            "email",
            "linkedin",
            "github",
            "order",
        ]


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            "title",
            "description",
            "date",
            "location",
            "status",
            "image",
            "registration_link",
        ]
        widgets = {
            "date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "description": forms.Textarea(attrs={"rows": 4}),
        }


class AdvisorForm(forms.ModelForm):
    class Meta:
        model = Advisor
        fields = [
            "name",
            "designation",
            "department",
            "photo",
            "bio",
            "email",
            "credentials",
        ]
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 4}),
            "credentials": forms.Textarea(attrs={"rows": 4}),
        }
