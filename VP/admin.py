from django.contrib import admin
from .models import Panel, Member, Advisor, Event, EventPhoto, EventResult, UserProfile


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
            "fields": ("name", "fathers_name", "email", "photo", "bio")
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


class EventPhotoInline(admin.TabularInline):
    model = EventPhoto
    extra = 1
    fields = ["order", "image", "caption"]


class EventResultInline(admin.TabularInline):
    model = EventResult
    extra = 1
    fields = ["order", "rank", "participant_name", "team_name"]


class EventAdmin(admin.ModelAdmin):
    list_display = ["title", "date", "status", "location"]
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


# Register models
admin.site.register(Panel, PanelAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(Advisor, AdvisorAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(EventPhoto, EventPhotoAdmin)
admin.site.register(EventResult, EventResultAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
