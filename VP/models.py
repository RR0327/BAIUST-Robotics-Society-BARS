from django.db import models
from django.contrib.auth.models import User

# from django.core.validators import FileExtensionValidator


class Panel(models.Model):
    name = models.CharField(max_length=100)
    year = models.CharField(max_length=50)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-year"]

    def __str__(self):
        return f"{self.name} ({self.year})"


class Member(models.Model):
    ROLES = [
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
        ("Member", "Member"),
    ]

    DEPARTMENTS = [
        ("CSE", "Computer Science & Engineering"),
        ("EEE", "Electrical & Electronic Engineering"),
        ("CE", "Civil Engineering"),
        ("BBA", "Business Administration"),
        ("LAW", "Law"),
    ]

    panel = models.ForeignKey(Panel, on_delete=models.CASCADE, related_name="members")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    fathers_name = models.CharField(max_length=100, null=True, blank=True)
    role = models.CharField(max_length=50, choices=ROLES)
    department = models.CharField(max_length=20, choices=DEPARTMENTS, default="CSE")
    photo = models.ImageField(upload_to="members/", blank=True, null=True)
    bio = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return f"{self.name} - {self.role}"


class Advisor(models.Model):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    photo = models.ImageField(upload_to="advisors/", blank=True, null=True)
    bio = models.TextField()
    email = models.EmailField()
    credentials = models.TextField(help_text="Enter each credential on a new line")

    def __str__(self):
        return self.name


class Event(models.Model):
    STATUS_CHOICES = [
        ("Upcoming", "Upcoming"),
        ("Ongoing", "Ongoing"),
        ("Completed", "Completed"),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    image = models.ImageField(upload_to="events/", blank=True, null=True)
    registration_link = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    USER_TYPES = [
        ("admin", "Admin/Advisor"),
        ("member", "Member"),
        ("student", "Student"),
        ("guest", "Guest"),
    ]
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="userprofile"
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default="student")
    panel = models.ForeignKey(Panel, on_delete=models.SET_NULL, null=True, blank=True)
    student_id = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.user_type}"
