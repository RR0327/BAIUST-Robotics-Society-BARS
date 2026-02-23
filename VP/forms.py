from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Panel, Member, Event, Advisor


class RegistrationForm(UserCreationForm):
    USER_TYPES = [
        ("student", "Student"),
        ("guest", "Guest"),
    ]

    user_type = forms.ChoiceField(
        choices=USER_TYPES,
        widget=forms.Select(
            attrs={
                "class": "form-select bg-dark text-light border-cyan",
                "id": "id_user_type",
                "style": "border: 1px solid var(--primary-cyan); border-radius: 5px;",
            }
        ),
        required=True,
        label="Account Type",
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control bg-dark text-light border-cyan",
                "placeholder": "example@email.com",
                "style": "border: 1px solid var(--primary-cyan); border-radius: 5px;",
            }
        ),
        label="Email Address",
    )

    student_id = forms.CharField(
        required=False,
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "class": "form-control bg-dark text-light border-cyan",
                "placeholder": "BAIUST-XX-XXX",
                "style": "border: 1px solid var(--primary-cyan); border-radius: 5px;",
            }
        ),
        label="Student ID",
    )

    phone = forms.CharField(
        required=False,
        max_length=20,
        widget=forms.TextInput(
            attrs={
                "class": "form-control bg-dark text-light border-cyan",
                "placeholder": "+8801XXXXXXXXX",
                "style": "border: 1px solid var(--primary-cyan); border-radius: 5px;",
            }
        ),
        label="Phone Number",
    )

    class Meta:
        model = User
        # UserCreationForm internally expects password1 and password2
        fields = ["username", "email", "user_type", "student_id", "phone"]
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "form-control bg-dark text-light border-cyan",
                    "placeholder": "Choose a username",
                    "style": "border: 1px solid var(--primary-cyan); border-radius: 5px;",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # FIXED: Accessing password1 instead of password to avoid KeyError
        self.fields["password1"].widget = forms.PasswordInput(
            attrs={
                "class": "form-control bg-dark text-light border-cyan",
                "placeholder": "Enter 8+ characters",
                "style": "border: 1px solid var(--primary-cyan); border-radius: 5px;",
            }
        )

        # FIXED: Accessing password2 instead of password_confirm
        self.fields["password2"].widget = forms.PasswordInput(
            attrs={
                "class": "form-control bg-dark text-light border-cyan",
                "placeholder": "Verify password",
                "style": "border: 1px solid var(--primary-cyan); border-radius: 5px;",
            }
        )

        # Unified Help Text and Labels
        self.fields["username"].help_text = (
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        )
        self.fields["password1"].label = "Password"
        self.fields["password1"].help_text = (
            "Your password must contain at least 8 characters."
        )
        self.fields["password2"].label = "Password Confirmation"
        self.fields["password2"].help_text = (
            "Enter the same password as before, for verification."
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": "form-control bg-dark text-light border-cyan",
                "placeholder": "Enter your username or email",
                "style": "border: 1px solid var(--primary-cyan); border-radius: 5px;",
            }
        ),
        label="Username or Email",
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control bg-dark text-light border-cyan",
                "placeholder": "Enter your password",
                "style": "border: 1px solid var(--primary-cyan); border-radius: 5px;",
            }
        ),
        label="Password",
    )

    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={"class": "form-check-input", "id": "rememberMe"}
        ),
        label="Remember me",
    )


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
        widgets = {
            "panel": forms.Select(
                attrs={
                    "class": "form-select bg-dark text-light border-cyan",
                    "style": "border: 1px solid var(--primary-cyan); border-radius: 5px;",
                }
            ),
            "name": forms.TextInput(
                attrs={
                    "class": "form-control bg-dark text-light border-cyan",
                    "placeholder": "Full Name",
                    "style": "border: 1px solid var(--primary-cyan); border-radius: 5px;",
                }
            ),
            "role": forms.Select(
                attrs={
                    "class": "form-select bg-dark text-light border-cyan",
                    "style": "border: 1px solid var(--primary-cyan); border-radius: 5px;",
                }
            ),
            "photo": forms.FileInput(
                attrs={
                    "class": "form-control bg-dark text-light border-cyan",
                    "style": "border: 1px solid var(--primary-cyan); border-radius: 5px;",
                }
            ),
            "bio": forms.Textarea(
                attrs={
                    "class": "form-control bg-dark text-light border-cyan",
                    "placeholder": "Member biography...",
                    "rows": 4,
                    "style": "border: 1px solid var(--primary-cyan); border-radius: 5px;",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control bg-dark text-light border-cyan",
                    "placeholder": "member@example.com",
                    "style": "border: 1px solid var(--primary-cyan); border-radius: 5px;",
                }
            ),
            "linkedin": forms.URLInput(
                attrs={
                    "class": "form-control bg-dark text-light border-cyan",
                    "placeholder": "https://linkedin.com/in/username",
                    "style": "border: 1px solid var(--primary-cyan); border-radius: 5px;",
                }
            ),
            "github": forms.URLInput(
                attrs={
                    "class": "form-control bg-dark text-light border-cyan",
                    "placeholder": "https://github.com/username",
                    "style": "border: 1px solid var(--primary-cyan); border-radius: 5px;",
                }
            ),
            "order": forms.NumberInput(
                attrs={
                    "class": "form-control bg-dark text-light border-cyan",
                    "style": "border: 1px solid var(--primary-cyan); border-radius: 5px;",
                    "min": "0",
                }
            ),
        }


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
            "title": forms.TextInput(
                attrs={
                    "class": "form-control bg-dark text-light border-cyan",
                    "placeholder": "Event Title",
                    "style": "border: 1px solid var(--primary-cyan); border-radius: 5px;",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control bg-dark text-light border-cyan",
                    "placeholder": "Event description...",
                    "rows": 4,
                    "style": "border: 1px solid var(--primary-cyan); border-radius: 5px;",
                }
            ),
            "date": forms.DateTimeInput(
                attrs={
                    "class": "form-control bg-dark text-light border-cyan",
                    "type": "datetime-local",
                    "style": "border: 1px solid var(--primary-cyan); border-radius: 5px;",
                }
            ),
            "location": forms.TextInput(
                attrs={
                    "class": "form-control bg-dark text-light border-cyan",
                    "placeholder": "Event Location",
                    "style": "border: 1px solid var(--primary-cyan); border-radius: 5px;",
                }
            ),
            "status": forms.Select(
                attrs={
                    "class": "form-select bg-dark text-light border-cyan",
                    "style": "border: 1px solid var(--primary-cyan); border-radius: 5px;",
                }
            ),
            "image": forms.FileInput(
                attrs={
                    "class": "form-control bg-dark text-light border-cyan",
                    "style": "border: 1px solid var(--primary-cyan); border-radius: 5px;",
                }
            ),
            "registration_link": forms.URLInput(
                attrs={
                    "class": "form-control bg-dark text-light border-cyan",
                    "placeholder": "https://forms.google.com/...",
                    "style": "border: 1px solid var(--primary-cyan); border-radius: 5px;",
                }
            ),
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
            "name": forms.TextInput(
                attrs={
                    "class": "form-control bg-dark text-light border-cyan",
                    "placeholder": "Full Name",
                    "style": "border: 1px solid var(--primary-cyan); border-radius: 5px;",
                }
            ),
            "designation": forms.TextInput(
                attrs={
                    "class": "form-control bg-dark text-light border-cyan",
                    "placeholder": "Professor, Lecturer, etc.",
                    "style": "border: 1px solid var(--primary-cyan); border-radius: 5px;",
                }
            ),
            "department": forms.TextInput(
                attrs={
                    "class": "form-control bg-dark text-light border-cyan",
                    "placeholder": "Department Name",
                    "style": "border: 1px solid var(--primary-cyan); border-radius: 5px;",
                }
            ),
            "photo": forms.FileInput(
                attrs={
                    "class": "form-control bg-dark text-light border-cyan",
                    "style": "border: 1px solid var(--primary-cyan); border-radius: 5px;",
                }
            ),
            "bio": forms.Textarea(
                attrs={
                    "class": "form-control bg-dark text-light border-cyan",
                    "placeholder": "Advisor biography...",
                    "rows": 4,
                    "style": "border: 1px solid var(--primary-cyan); border-radius: 5px;",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control bg-dark text-light border-cyan",
                    "placeholder": "advisor@baiust.edu.bd",
                    "style": "border: 1px solid var(--primary-cyan); border-radius: 5px;",
                }
            ),
            "credentials": forms.Textarea(
                attrs={
                    "class": "form-control bg-dark text-light border-cyan",
                    "placeholder": "Enter each credential on a new line...",
                    "rows": 4,
                    "style": "border: 1px solid var(--primary-cyan); border-radius: 5px;",
                }
            ),
        }


class PanelForm(forms.ModelForm):
    class Meta:
        model = Panel
        fields = ["name", "year", "description"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control bg-dark text-light border-cyan",
                    "placeholder": "Panel Name",
                    "style": "border: 1px solid var(--primary-cyan); border-radius: 5px;",
                }
            ),
            "year": forms.TextInput(
                attrs={
                    "class": "form-control bg-dark text-light border-cyan",
                    "placeholder": "2024-2025",
                    "style": "border: 1px solid var(--primary-cyan); border-radius: 5px;",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control bg-dark text-light border-cyan",
                    "placeholder": "Panel achievements...",
                    "rows": 4,
                    "style": "border: 1px solid var(--primary-cyan); border-radius: 5px;",
                }
            ),
        }


class UserUpdateForm(forms.ModelForm):
    """Form to update basic User information."""

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "form-control bg-dark text-light border-cyan",
                    "style": "border: 1px solid var(--primary-cyan); border-radius: 5px;",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control bg-dark text-light border-cyan",
                    "style": "border: 1px solid var(--primary-cyan); border-radius: 5px;",
                }
            ),
            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control bg-dark text-light border-cyan",
                    "style": "border: 1px solid var(--primary-cyan); border-radius: 5px;",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control bg-dark text-light border-cyan",
                    "style": "border: 1px solid var(--primary-cyan); border-radius: 5px;",
                }
            ),
        }


class UserProfileForm(forms.ModelForm):
    """Form to update specific BARS Profile information."""

    class Meta:
        model = UserProfile
        fields = ["user_type", "panel", "student_id", "phone"]
        widgets = {
            "user_type": forms.Select(
                attrs={"class": "form-select bg-dark text-light border-cyan"}
            ),
            "panel": forms.Select(
                attrs={"class": "form-select bg-dark text-light border-cyan"}
            ),
            "student_id": forms.TextInput(
                attrs={
                    "class": "form-control bg-dark text-light border-cyan",
                    "placeholder": "Student ID",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "form-control bg-dark text-light border-cyan",
                    "placeholder": "Phone Number",
                }
            ),
        }
