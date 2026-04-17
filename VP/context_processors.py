from .models import GeneralMemberApplication


def general_member_application(request):
    application = GeneralMemberApplication.objects.first()
    return {
        "general_member_application": application,
    }
