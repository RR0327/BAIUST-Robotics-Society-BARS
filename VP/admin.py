from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError
from .models import (
    Panel,
    Member,
    Advisor,
    Event,
    EventPhoto,
    EventResult,
    Achievement,
    GeneralMemberApplication,
    UserProfile,
)


class UserProfileAdminForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        is_bars_member = cleaned_data.get("is_bars_member")
        position_name = cleaned_data.get("position_name")

        if is_bars_member and not position_name:
            raise ValidationError({
                "position_name": "Position Name is required when user is a BARS member."
            })

        if not is_bars_member:
            cleaned_data["position_name"] = None

        return cleaned_data


class PanelAdmin(admin.ModelAdmin):
    list_display = ["name", "year", "created_at"]
    list_filter = ["year", "created_at"]
    search_fields = ["name", "description"]
    ordering = ["-year"]


class MemberAdmin(admin.ModelAdmin):
    list_display = ["name", "role", "department", "panel", "email", "mobile_number", "order"]
    list_filter = ["role", "department", "panel"]
    search_fields = ["name", "email", "mobile_number", "bio"]
    ordering = ["order", "name"]
    fieldsets = (
        ("Personal Information", {
            "fields": ("name", "fathers_name", "email", "mobile_number", "photo", "bio")
        }),
        ("Role & Panel", {
            "fields": ("role", "panel", "department", "order")
        }),
        ("Social & Links", {
            "fields": ("linkedin", "github")
        }),
        ("User Account", {
            "fields": ("user",),
            "classes": ("collapse",)
        }),
    )


class AdvisorAdmin(admin.ModelAdmin):
    list_display = ["name", "designation", "department", "email"]
    list_filter = ["department"]
    search_fields = ["name", "designation", "department", "email", "expertise"]
    fieldsets = (
        ("Basic Information", {
            "fields": ("name", "designation", "department", "photo")
        }),
        ("Contact & Bio", {
            "fields": ("email", "bio")
        }),
        ("Expertise", {
            "fields": ("expertise",)
        }),
        ("Credentials", {
            "fields": ("credentials",)
        }),
    )


class EventPhotoInline(admin.TabularInline):
    model = EventPhoto
    extra = 1
    fields = ["order", "image", "caption"]


class EventResultInline(admin.TabularInline):
    model = EventResult
    extra = 1
    fields = ["order", "rank", "participant_name", "team_name"]


class EventAdmin(admin.ModelAdmin):
    list_display = ["title", "date", "end_date", "status", "location"]
    list_filter = ["status", "date", "created_at"]
    search_fields = ["title", "description", "location"]
    ordering = ["-date"]
    readonly_fields = ["created_at"]
    inlines = [EventPhotoInline, EventResultInline]
    fieldsets = (
        ("Event Information", {
            "fields": ("title", "description", "image")
        }),
        ("Details", {
            "fields": ("date", "end_date", "location", "status")
        }),
        ("Registration", {
            "fields": ("registration_link",)
        }),
        ("Metadata", {
            "fields": ("created_at",),
            "classes": ("collapse",)
        }),
    )


class UserProfileAdmin(admin.ModelAdmin):
    form = UserProfileAdminForm
    list_display = [
        "user",
        "user_type",
        "is_bars_member",
        "position_name",
        "panel",
        "student_id",
    ]
    list_filter = ["user_type", "is_bars_member", "position_name", "panel", "created_at"]
    search_fields = [
        "user__username",
        "user__email",
        "student_id",
        "phone",
        "position_name",
    ]
    ordering = ["-created_at"]
    readonly_fields = ["created_at"]

    fieldsets = (
        ("User Account", {
            "fields": ("user", "user_type")
        }),
        ("Profile Information", {
            "fields": (
                "is_bars_member",
                "position_name",
                "panel",
                "student_id",
                "phone",
            )
        }),
        ("Metadata", {
            "fields": ("created_at",),
            "classes": ("collapse",)
        }),
    )


class EventPhotoAdmin(admin.ModelAdmin):
    list_display = ["__str__", "event", "order", "caption", "uploaded_at"]
    list_filter = ["event", "uploaded_at"]
    search_fields = ["caption", "event__title"]
    ordering = ["event", "order", "uploaded_at"]
    list_editable = ["order"]


class EventResultAdmin(admin.ModelAdmin):
    list_display = ["event", "rank", "participant_name", "team_name", "order"]
    list_filter = ["event", "rank"]
    search_fields = ["participant_name", "team_name", "event__title"]
    ordering = ["event", "order"]
    list_editable = ["order"]


class AchievementAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "category",
        "position",
        "contest_name",
        "date",
        "order",
    ]
    list_filter = ["category", "date", "created_at"]
    search_fields = ["title", "contest_name", "team_name", "participants"]
    ordering = ["order", "-date", "-created_at"]
    list_editable = ["order"]
    fieldsets = (
        (
            "Achievement Details",
            {
                "fields": (
                    "title",
                    "category",
                    "contest_name",
                    "position",
                    "team_name",
                )
            },
        ),
        ("Participants", {"fields": ("participants",)}),
        ("Description", {"fields": ("description",)}),
        ("Media & Context", {"fields": ("image", "date", "location")}),
        ("Ordering", {"fields": ("order",)}),
        ("Metadata", {"fields": ("created_at",), "classes": ("collapse",)}),
    )
    readonly_fields = ["created_at"]


class GeneralMemberApplicationAdmin(admin.ModelAdmin):
    list_display = ["title", "is_active", "form_url"]
    list_filter = ["is_active"]
    search_fields = ["title", "form_url"]
    fieldsets = (
        ("Application Link", {
            "fields": ("title", "form_url", "is_active")
        }),
    )


# Register models
admin.site.register(Panel, PanelAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(Advisor, AdvisorAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(EventPhoto, EventPhotoAdmin)
admin.site.register(EventResult, EventResultAdmin)
admin.site.register(Achievement, AchievementAdmin)
admin.site.register(GeneralMemberApplication, GeneralMemberApplicationAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
