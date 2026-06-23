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
        self.assertIn("Your registration was submitted successfully and is pending approval.", messages)
        
        # Follow the redirect and verify context
        redirect_response = self.client.get(reverse("event_detail", args=[self.event.id]))
        self.assertTrue(redirect_response.context['is_registered'])
        self.assertEqual(redirect_response.context['registration'].status, 'Pending')
        
        # Assert registration created but no QR code / email yet
        self.assertEqual(EventRegistration.objects.count(), 1)
        registration = EventRegistration.objects.first()
        self.assertEqual(registration.user, self.user)
        self.assertEqual(registration.event, self.event)
        self.assertIsNone(registration.serial_no)
        self.assertFalse(bool(registration.qr_code))
        self.assertEqual(len(mail.outbox), 0)
        
        # Now, simulate admin approval to trigger email & ticket generation
        admin_user = User.objects.create_superuser(username="adminuser2", email="admin2@example.com", password="password")
        self.client.login(username="adminuser2", password="password")
        approve_url = reverse("approve_registration", args=[registration.id])
        approve_response = self.client.get(approve_url)
        self.assertEqual(approve_response.status_code, 302)
        
        # Reload registration
        registration.refresh_from_db()
        self.assertEqual(registration.status, 'Approved')
        self.assertEqual(registration.serial_no, 1)
        self.assertTrue(bool(registration.qr_code))
        
        # Verify email sent
        self.assertEqual(len(mail.outbox), 1)
        sent_email = mail.outbox[0]
        
        # Check subject and recipient
        self.assertEqual(sent_email.subject, "🎟 Your Event Ticket is Ready for Robotics Workshop")
        self.assertEqual(sent_email.to, ["testuser@example.com"])
        
        # Check body contents
        expected_body = (
            "Hello Test User,\n\n"
            "Your registration for 'Robotics Workshop' has been APPROVED!\n"
            "Your digital ticket has been generated.\n\n"
            "Please find your digital ticket stub attached as a PDF to this email. Present this ticket at the event entrance.\n\n"
            "Thanks,\n"
            "BAIUST Robotics Society"
        )
        self.assertEqual(sent_email.body, expected_body)
        
        # Verify attachment
        self.assertEqual(len(sent_email.attachments), 1)
        attachment_name, attachment_content, content_type = sent_email.attachments[0]
        self.assertEqual(attachment_name, f"Ticket_{registration.id}.pdf")
        self.assertEqual(content_type, "application/pdf")
        
        # Clean up the generated QR Code file
        registration.qr_code.delete(save=False)

    def test_registration_with_custom_fields(self):
        self.client.login(username="testuser", password="testpassword123")
        
        from django.core.files.uploadedfile import SimpleUploadedFile
        test_image = SimpleUploadedFile(
            name='test_photo.jpg', 
            content=b'dummy_image_data', 
            content_type='image/jpeg'
        )
        
        post_data = {
            "name": "Jane Doe",
            "student_id": "CSE-2024-001",
            "email": "janedoe@example.com",
            "phone": "01712345678",
            "payment_method": "bkash",
            "transaction_id": "TXN998877",
            "photo": test_image
        }
        
        response = self.client.post(self.url, post_data)
        self.assertEqual(response.status_code, 302)
        
        registration = EventRegistration.objects.first()
        self.assertEqual(registration.name, "Jane Doe")
        self.assertEqual(registration.student_id, "CSE-2024-001")
        self.assertEqual(registration.email, "janedoe@example.com")
        self.assertEqual(registration.phone, "01712345678")
        self.assertEqual(registration.payment_method, "bkash")
        self.assertEqual(registration.transaction_id, "TXN998877")
        self.assertIsNone(registration.hand_cash_recipient)
        self.assertTrue(bool(registration.photo))
        
        # Clean up files
        registration.qr_code.delete(save=False)
        registration.photo.delete(save=False)


class LoginEmailOrUsernameTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword123"
        )
        self.login_url = reverse("login")

    def test_login_with_username(self):
        response = self.client.post(self.login_url, {
            "username": "testuser",
            "password": "testpassword123"
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.wsgi_request.user, self.user)

    def test_login_with_email(self):
        response = self.client.post(self.login_url, {
            "username": "testuser@example.com",
            "password": "testpassword123"
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.wsgi_request.user, self.user)

    def test_login_with_email_case_insensitive(self):
        response = self.client.post(self.login_url, {
            "username": "TESTUSER@EXAMPLE.COM",
            "password": "testpassword123"
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.wsgi_request.user, self.user)

    def test_login_with_invalid_username(self):
        response = self.client.post(self.login_url, {
            "username": "invaliduser",
            "password": "testpassword123"
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_login_with_invalid_email(self):
        response = self.client.post(self.login_url, {
            "username": "invalidemail@example.com",
            "password": "testpassword123"
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_login_with_invalid_password(self):
        response = self.client.post(self.login_url, {
            "username": "testuser",
            "password": "wrongpassword"
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)


class TicketPdfDownloadTest(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            username="owneruser",
            email="owner@example.com",
            password="testpassword123"
        )
        self.non_owner = User.objects.create_user(
            username="otheruser",
            email="other@example.com",
            password="testpassword123"
        )
        self.admin_user = User.objects.create_superuser(
            username="adminuser",
            email="admin@example.com",
            password="testpassword123"
        )
        
        self.event = Event.objects.create(
            title="Robotics Workshop",
            description="Learn to build robots.",
            date=timezone.now() + timezone.timedelta(days=2),
            location="Lab 1",
            status="Upcoming",
            capacity=10
        )
        
        self.registration = EventRegistration.objects.create(
            user=self.owner,
            event=self.event,
            name="Owner Attendee",
            email="owner@example.com",
            phone="01711111111"
        )
        
        self.url = reverse("download_ticket_pdf", args=[self.registration.id])

    def tearDown(self):
        if self.registration.qr_code:
            self.registration.qr_code.delete(save=False)

    def test_anonymous_user_cannot_download(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_owner_can_download(self):
        self.client.login(username="owneruser", password="testpassword123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertTrue(response['Content-Disposition'].startswith('attachment; filename="Ticket_'))

    def test_admin_can_download(self):
        self.client.login(username="adminuser", password="testpassword123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')

    def test_non_owner_cannot_download(self):
        self.client.login(username="otheruser", password="testpassword123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)


class EventRegistrationSerialNoTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="password")
        self.user2 = User.objects.create_user(username="user2", password="password")
        self.user3 = User.objects.create_user(username="user3", password="password")
        
        self.event1 = Event.objects.create(
            title="Event 1",
            description="First Event",
            date=timezone.now() + timezone.timedelta(days=2),
            location="Room 101",
            status="Upcoming"
        )
        self.event2 = Event.objects.create(
            title="Event 2",
            description="Second Event",
            date=timezone.now() + timezone.timedelta(days=3),
            location="Room 102",
            status="Upcoming"
        )

    def test_serial_no_generation_per_event(self):
        # Register user1 to event1 -> serial_no should be 1
        reg1 = EventRegistration.objects.create(user=self.user1, event=self.event1, status='Approved')
        self.assertEqual(reg1.serial_no, 1)

        # Register user2 to event1 -> serial_no should be 2
        reg2 = EventRegistration.objects.create(user=self.user2, event=self.event1, status='Approved')
        self.assertEqual(reg2.serial_no, 2)

        # Register user3 to event2 -> serial_no should be 1 (different event)
        reg3 = EventRegistration.objects.create(user=self.user3, event=self.event2, status='Approved')
        self.assertEqual(reg3.serial_no, 1)


class EventRegistrationApprovalTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="registrant", password="password")
        self.admin = User.objects.create_superuser(username="adminuser", email="admin@example.com", password="password")
        
        self.event = Event.objects.create(
            title="Workshop",
            description="Learn things",
            date=timezone.now() + timezone.timedelta(days=2),
            location="Lab 2",
            status="Upcoming",
            capacity=10
        )

    def test_approval_workflow(self):
        # Create a new registration
        reg = EventRegistration.objects.create(user=self.user, event=self.event)
        self.assertEqual(reg.status, 'Pending')
        self.assertIsNone(reg.serial_no)
        self.assertFalse(bool(reg.qr_code))

        # Approve registration
        self.client.login(username="adminuser", password="password")
        approve_url = reverse("approve_registration", args=[reg.id])
        response = self.client.get(approve_url)
        self.assertEqual(response.status_code, 302) # Redirect to dashboard

        # Reload from DB
        reg.refresh_from_db()
        self.assertEqual(reg.status, 'Approved')
        self.assertEqual(reg.serial_no, 1)
        self.assertTrue(bool(reg.qr_code))

        # Reject registration
        reject_url = reverse("reject_registration", args=[reg.id])
        response = self.client.get(reject_url)
        self.assertEqual(response.status_code, 302)

        # Reload from DB
        reg.refresh_from_db()
        self.assertEqual(reg.status, 'Rejected')
        self.assertIsNone(reg.serial_no)
        self.assertFalse(bool(reg.qr_code))


