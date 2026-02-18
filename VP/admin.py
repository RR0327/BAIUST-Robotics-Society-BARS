from django.contrib import admin
from .models import Panel, Member, Advisor, Event, UserProfile


class PanelAdmin(admin.ModelAdmin):
    list_display = ["name", "year", "created_at"]
    list_filter = ["year", "created_at"]
    search_fields = ["name", "description"]
    ordering = ["-year"]


class MemberAdmin(admin.ModelAdmin):
    list_display = ["name", "role", "department", "panel", "email", "order"]
    list_filter = ["role", "department", "panel"]
    search_fields = ["name", "email", "bio"]
    ordering = ["order", "name"]
    fieldsets = (
        ("Personal Information", {
            "fields": ("name", "email", "photo", "bio")
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
    search_fields = ["name", "designation", "department", "email"]
    fieldsets = (
        ("Basic Information", {
            "fields": ("name", "designation", "department", "photo")
        }),
        ("Contact & Bio", {
            "fields": ("email", "bio")
        }),
        ("Credentials", {
            "fields": ("credentials",)
        }),
    )


class EventAdmin(admin.ModelAdmin):
    list_display = ["title", "date", "status", "location"]
    list_filter = ["status", "date", "created_at"]
    search_fields = ["title", "description", "location"]
    ordering = ["-date"]
    fieldsets = (
        ("Event Information", {
            "fields": ("title", "description", "image")
        }),
        ("Details", {
            "fields": ("date", "location", "status")
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
    list_display = ["user", "user_type", "panel", "student_id"]
    list_filter = ["user_type", "panel", "created_at"]
    search_fields = ["user__username", "user__email", "student_id", "phone"]
    ordering = ["-created_at"]
    fieldsets = (
        ("User Account", {
            "fields": ("user", "user_type")
        }),
        ("Profile Information", {
            "fields": ("panel", "student_id", "phone")
        }),
        ("Metadata", {
            "fields": ("created_at",),
            "classes": ("collapse",)
        }),
    )


# Register models
admin.site.register(Panel, PanelAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(Advisor, AdvisorAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
