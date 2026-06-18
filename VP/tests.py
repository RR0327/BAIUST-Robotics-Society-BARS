from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.core import mail
from django.utils import timezone
from VP.models import Event, EventRegistration

class EventRegistrationEmailTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword123",
            first_name="Test",
            last_name="User"
        )
        self.event = Event.objects.create(
            title="Robotics Workshop",
            description="Learn to build robots.",
            date=timezone.now() + timezone.timedelta(days=2),
            location="Lab 1",
            status="Upcoming",
            capacity=10
        )
        self.url = reverse("register_event", args=[self.event.id])

    def test_registration_sends_email(self):
        # Log in the user
        self.client.login(username="testuser", password="testpassword123")
        
        # Verify no registration or email sent yet
        self.assertEqual(EventRegistration.objects.count(), 0)
        self.assertEqual(len(mail.outbox), 0)
        
        # Post to the registration URL
        response = self.client.post(self.url)
        
        # Assert redirect to event detail
        self.assertRedirects(response, reverse("event_detail", args=[self.event.id]))
        
        # Check that the success message is present in the redirect response
        from django.contrib.messages import get_messages
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn("Your registration has been successfully.", messages)
        
        # Follow the redirect and verify context
        redirect_response = self.client.get(reverse("event_detail", args=[self.event.id]))
        self.assertTrue(redirect_response.context['is_registered'])
        self.assertEqual(redirect_response.context['registration'].user, self.user)
        
        # Assert registration created
        self.assertEqual(EventRegistration.objects.count(), 1)
        registration = EventRegistration.objects.first()
        self.assertEqual(registration.user, self.user)
        self.assertEqual(registration.event, self.event)
        
        # Verify QR Code was generated and exists
        self.assertTrue(bool(registration.qr_code))
        self.assertTrue(registration.qr_code.name.startswith("registrations/ticket_qr_"))
        self.assertTrue(registration.qr_code.storage.exists(registration.qr_code.name))
        
        # Assert context contains registration and response renders the QR code image url
        self.assertEqual(redirect_response.context['registration'], registration)
        self.assertContains(redirect_response, registration.qr_code.url)
        
        # Clean up the generated QR Code file to avoid leaving dummy files in media directory
        registration.qr_code.delete(save=False)
        
        # Assert email sent
        self.assertEqual(len(mail.outbox), 1)
        sent_email = mail.outbox[0]
        
        # Check subject and recipient
        self.assertEqual(sent_email.subject, "🎟 Your Event Ticket is Ready for Robotics Workshop")
        self.assertEqual(sent_email.to, ["testuser@example.com"])
        
        # Check body contents
        expected_body = (
            "Hello Test User\n\n"
            "You're registered for: Robotics Workshop\n"
            "Your digital ticket has been generated.\n\n"
            "Thanks,\n"
            "BAIUST Robotics Society"
        )
        self.assertEqual(sent_email.body, expected_body)
