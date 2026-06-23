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
    EventRegistration,
)
from .views import (
    generate_csv_response,
    generate_json_response,
    generate_excel_response,
    generate_pdf_response,
)


def export_selected_to_csv(modeladmin, request, queryset):
    """Admin action to export selected records to CSV format."""
    model_name = queryset.model.__name__.lower()
    resource = "members" if model_name == "member" else ("events" if model_name == "event" else "registrations")
    return generate_csv_response(resource, queryset)
export_selected_to_csv.short_description = "Export selected to CSV"


def export_selected_to_json(modeladmin, request, queryset):
    """Admin action to export selected records to JSON format."""
    model_name = queryset.model.__name__.lower()
    resource = "members" if model_name == "member" else ("events" if model_name == "event" else "registrations")
    return generate_json_response(resource, queryset)
export_selected_to_json.short_description = "Export selected to JSON"


def export_selected_to_excel(modeladmin, request, queryset):
    """Admin action to export selected records to Excel (XLSX) format."""
    model_name = queryset.model.__name__.lower()
    resource = "members" if model_name == "member" else ("events" if model_name == "event" else "registrations")
    return generate_excel_response(resource, queryset)
export_selected_to_excel.short_description = "Export selected to Excel (XLSX)"


def export_selected_to_pdf(modeladmin, request, queryset):
    """Admin action to export selected records to PDF format."""
    model_name = queryset.model.__name__.lower()
    resource = "members" if model_name == "member" else ("events" if model_name == "event" else "registrations")
    return generate_pdf_response(resource, queryset)
export_selected_to_pdf.short_description = "Export selected to PDF (BARS Branded)"


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
    actions = [export_selected_to_csv, export_selected_to_json, export_selected_to_excel, export_selected_to_pdf]
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
    list_display = ["title", "date", "end_date", "registration_deadline", "capacity", "status", "location", "registration_count"]
    actions = [export_selected_to_csv, export_selected_to_json, export_selected_to_excel, export_selected_to_pdf]
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
            "fields": ("registration_link", "registration_deadline", "capacity")
        }),
        ("Metadata", {
            "fields": ("created_at",),
            "classes": ("collapse",)
        }),
    )

    def registration_count(self, obj):
        return obj.registrations.count()
    registration_count.short_description = "Registrations"


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
    actions = [export_selected_to_csv, export_selected_to_json, export_selected_to_excel, export_selected_to_pdf]
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


class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ["serial_no", "user", "event", "status", "registered_at"]
    list_filter = ["status", "event", "registered_at"]
    search_fields = ["user__username", "user__email", "event__title"]
    ordering = ["-registered_at"]


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
admin.site.register(EventRegistration, EventRegistrationAdmin)
