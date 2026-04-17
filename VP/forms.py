from django import forms
import re
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile, Panel, Member, Event, Advisor


class RegistrationForm(UserCreationForm):
    USER_TYPES = [
        ("student", "Student"),
        ("guest", "Guest"),
    ]
    BARS_MEMBER_CHOICES = [
        ("yes", "Yes"),
        ("no", "No"),
    ]
    POSITION_CHOICES = [
        ("", "Select Position"),
        ("President", "President"),
        ("Vice President", "Vice President"),
        ("General Secretary", "General Secretary"),
        ("Joint Secretary", "Joint Secretary"),
        ("Treasurer", "Treasurer"),
        ("Assistant Treasurer", "Assistant Treasurer"),
        ("Organizing Secretary", "Organizing Secretary"),
        ("Assistant Organizing Secretary", "Assistant Organizing Secretary"),
        ("Media & Publication Secretary", "Media & Publication Secretary"),
        (
            "Assistant Media & Publication Secretary",
            "Assistant Media & Publication Secretary",
        ),
        ("Executive Member", "Executive Member"),
        ("General Member", "General Member"),
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
        required=True,
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "class": "form-control bg-dark text-light border-cyan",
                "placeholder": "BAIUST-STUDENT-ID",
                "style": "border: 1px solid var(--primary-cyan); border-radius: 5px;",
            }
        ),
        label="Student ID",
    )

    phone = forms.CharField(
        required=True,
        max_length=20,
        widget=forms.TextInput(
            attrs={
                "class": "form-control bg-dark text-light border-cyan",
                "placeholder": "01XXXXXXXXX",
                "style": "border: 1px solid var(--primary-cyan); border-radius: 5px;",
            }
        ),
        label="Phone Number",
    )

    is_bars_member = forms.ChoiceField(
        choices=BARS_MEMBER_CHOICES,
        widget=forms.RadioSelect(
            attrs={
                "class": "form-check-input",
            }
        ),
        required=True,
        initial="yes",
        label="Are you a BARS member?",
    )

    position_name = forms.ChoiceField(
        choices=POSITION_CHOICES,
        required=True,
        widget=forms.Select(
            attrs={
                "class": "form-select bg-dark text-light border-cyan",
                "style": "border: 1px solid var(--primary-cyan); border-radius: 5px;",
                "id": "id_position_name",
            }
        ),
        initial="",
        label="Position Name",
    )

    class Meta:
        model = User
        # UserCreationForm internally expects password1 and password2
        fields = [
            "username",
            "email",
            "user_type",
            "student_id",
            "phone",
            "is_bars_member",
            "position_name",
        ]
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
                "placeholder": "Enter your password",
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

    def clean_email(self):
        email = self.cleaned_data["email"].strip()

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "This email is already registered. Please use a different email."
            )

        return email

    def clean_student_id(self):
        student_id = self.cleaned_data.get("student_id", "").strip()

        if student_id and UserProfile.objects.filter(student_id__iexact=student_id).exists():
            raise forms.ValidationError(
                "This student ID is already registered. Please use a different ID."
            )

        return student_id

    def clean_phone(self):
        phone = self.cleaned_data.get("phone", "").strip()
        normalized_phone = re.sub(r"[()\s-]", "", phone)

        if normalized_phone and UserProfile.objects.filter(phone=normalized_phone).exists():
            raise forms.ValidationError(
                "This phone number is already registered. Please use a different number."
            )

        return normalized_phone

    def clean(self):
        cleaned_data = super().clean()
        is_bars_member = cleaned_data.get("is_bars_member", "yes")
        position_name = cleaned_data.get("position_name")

        if is_bars_member == "yes" and not position_name:
            self.add_error("position_name", "Please select a position name.")

        if is_bars_member == "no":
            cleaned_data["position_name"] = None

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"].lower()
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs.update(
            {
                "class": "form-control bg-dark text-light border-cyan",
                "placeholder": "Enter your username or email",
                "style": "border: 1px solid var(--primary-cyan); border-radius: 5px;",
            }
        )
        self.fields["password"].widget.attrs.update(
            {
                "class": "form-control bg-dark text-light border-cyan",
                "placeholder": "Enter your password",
                "style": "border: 1px solid var(--primary-cyan); border-radius: 5px;",
            }
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
            "expertise",
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
            "expertise": forms.Textarea(
                attrs={
                    "class": "form-control bg-dark text-light border-cyan",
                    "placeholder": "One expertise per line (e.g. Robotics, AI, Embedded Systems)...",
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

    def clean_expertise(self):
        expertise = self.cleaned_data.get("expertise", "")
        return Advisor.normalize_bullet_lines(expertise)


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
        fields = ["user_type", "student_id", "phone"]
        widgets = {
            "user_type": forms.Select(
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

    def clean_student_id(self):
        student_id = self.cleaned_data.get("student_id", "").strip()

        if not student_id:
            return student_id

        qs = UserProfile.objects.filter(student_id__iexact=student_id)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError(
                "This student ID is already in use."
            )

        return student_id

    def clean_phone(self):
        phone = self.cleaned_data.get("phone", "").strip()
        normalized_phone = re.sub(r"[()\s-]", "", phone)

        if not normalized_phone:
            return normalized_phone

        qs = UserProfile.objects.filter(phone=normalized_phone)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError(
                "This phone number is already in use."
            )

        return normalized_phone
