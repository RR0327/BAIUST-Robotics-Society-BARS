import re
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

    @property
    def president_count(self):
        # Prefer explicit Member records; fallback to a panel admin profile.
        member_presidents = self.members.filter(role__iexact="President").count()
        if member_presidents:
            return member_presidents
        return 1 if self.userprofile_set.filter(user_type="admin").exists() else 0

    @property
    def total_member_count(self):
        total = self.members.count()
        has_member_president = self.members.filter(role__iexact="President").exists()
        has_admin_president = self.userprofile_set.filter(user_type="admin").exists()
        if not has_member_president and has_admin_president:
            total += 1
        return total

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
    mobile_number = models.CharField(max_length=11, blank=True, null=True)
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
    bio = models.TextField(blank=True, null=True)
    expertise = models.TextField(
        blank=True,
        help_text="Enter one expertise per line (bullet points are optional)",
    )
    email = models.EmailField()
    credentials = models.TextField(help_text="Enter each credential on a new line")

    def __str__(self):
        return self.name

    @staticmethod
    def normalize_bullet_lines(raw_text):
        if not raw_text:
            return ""

        points = []
        for line in str(raw_text).replace("\r\n", "\n").split("\n"):
            cleaned = line.strip()
            if not cleaned:
                continue

            # Accept pasted bullets/numbers and keep only normalized text.
            cleaned = re.sub(r"^[-*\u2022]+\s*", "", cleaned)
            cleaned = re.sub(r"^\d+[.)\-\s]+", "", cleaned)
            if cleaned:
                points.append(cleaned)

        return "\n".join(points)

    @property
    def expertise_points(self):
        return [line.strip() for line in self.expertise.split("\n") if line.strip()]

    def save(self, *args, **kwargs):
        self.expertise = self.normalize_bullet_lines(self.expertise)
        super().save(*args, **kwargs)


class Event(models.Model):
    STATUS_CHOICES = [
        ("Upcoming", "Upcoming"),
        ("Ongoing", "Ongoing"),
        ("Completed", "Completed"),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    image = models.ImageField(upload_to="events/", blank=True, null=True)
    registration_link = models.URLField(blank=True)
    registration_deadline = models.DateTimeField(null=True, blank=True)
    capacity = models.PositiveIntegerField(null=True, blank=True, help_text="Leave blank or set to null for unlimited seats.")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return self.title

    @property
    def is_registration_open(self):
        from django.utils import timezone
        if self.status != "Upcoming":
            return False
        if timezone.now() >= self.date:
            return False
        if self.registration_deadline and timezone.now() > self.registration_deadline:
            return False
        if self.capacity is not None and self.registration_count >= self.capacity:
            return False
        return True

    @property
    def registration_count(self):
        return self.registrations.count()

    @property
    def remaining_seats(self):
        if self.capacity is None:
            return None
        return max(0, self.capacity - self.registration_count)


class EventPhoto(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="photos")
    image = models.ImageField(upload_to="events/photos/", blank=True, null=True)
    caption = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "uploaded_at"]

    def __str__(self):
        if self.caption:
            return self.event.title + " - " + self.caption
        return f"{self.event.title} - Photo #{self.id}"


class EventResult(models.Model):
    RANK_CHOICES = [
        ("Champion", "Champion"),
        ("1st Runner-up", "1st Runner-up"),
        ("2nd Runner-up", "2nd Runner-up"),
        ("3rd Place", "3rd Place"),
        ("4th Place", "4th Place"),
        ("5th Place", "5th Place"),
        ("6th Place", "6th Place"),
        ("7th Place", "7th Place"),
        ("8th Place", "8th Place"),
        ("9th Place", "9th Place"),
        ("10th Place", "10th Place"),
    ]
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="results")
    rank = models.CharField(max_length=50, choices=RANK_CHOICES)
    participant_name = models.CharField(max_length=200)
    team_name = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.event.title} - {self.rank}: {self.participant_name}"


class EventRegistration(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="event_registrations")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="registrations")
    name = models.CharField(max_length=100, blank=True)
    student_id = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    photo = models.ImageField(upload_to="registrations/photos/", null=True, blank=True)
    payment_method = models.CharField(max_length=20, choices=[('bkash', 'bKash'), ('hand_cash', 'Hand Cash')], default='hand_cash')
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    hand_cash_recipient = models.CharField(max_length=100, null=True, blank=True)
    registered_at = models.DateTimeField(auto_now_add=True)
    qr_code = models.ImageField(upload_to="registrations/", blank=True, null=True)
    serial_no = models.PositiveIntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Approved')

    class Meta:
        unique_together = ('user', 'event')
        ordering = ['-registered_at']

    def __str__(self):
        return f"{self.user.username} registered for {self.event.title}"

    def generate_qr_code(self):
        import qrcode
        from io import BytesIO
        from django.core.files import File
        
        # Clean up any existing QR code file to prevent filename suffixes/duplicates on regenerate
        if self.qr_code:
            try:
                self.qr_code.delete(save=False)
            except Exception:
                pass

        qr_content = f"Registration ID: {self.id} | Serial No: {self.serial_no} | User: {self.user.username} | Event: {self.event.title}"
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(qr_content)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        filename = f"ticket_qr_{self.id}.png"
        self.qr_code.save(filename, File(buffer), save=False)
        # Avoid recursion by updating only the qr_code column directly
        EventRegistration.objects.filter(pk=self.pk).update(qr_code=self.qr_code.name)

    def save(self, *args, **kwargs):
        is_approved = self.status == 'Approved'
        was_approved = False
        if self.pk:
            try:
                orig = EventRegistration.objects.get(pk=self.pk)
                was_approved = orig.status == 'Approved'
            except EventRegistration.DoesNotExist:
                pass
            
        if is_approved:
            if not was_approved or not self.serial_no:
                max_serial = EventRegistration.objects.filter(event=self.event, status='Approved').aggregate(
                    max_serial=models.Max('serial_no')
                )['max_serial']
                self.serial_no = (max_serial or 0) + 1
        else:
            self.serial_no = None
            if self.qr_code:
                try:
                    self.qr_code.delete(save=False)
                except Exception:
                    pass
                self.qr_code = None
                
        super().save(*args, **kwargs)
        if is_approved and not self.qr_code:
            self.generate_qr_code()


class Achievement(models.Model):
    CATEGORY_CHOICES = [
        ("club", "Club Performance"),
        ("contest", "Outside Contest"),
        ("research", "Research/Publication"),
        ("innovation", "Innovation"),
        ("autonomous_robot_challenge", "Autonomous Robot Challenge"),
        ("line_following_robot_competition", "Line Following Robot Competition"),
        ("maze_solving_robot", "Maze Solving Robot"),
        ("robo_soccer", "Robo Soccer"),
        ("robo_race", "Robo Race"),
        ("combat_robotics_battle_bots", "Combat Robotics (Battle Bots)"),
        ("drone_racing_uav_competition", "Drone Racing / UAV Competition"),
        ("other", "Other"),
    ]

    title = models.CharField(max_length=200)
    contest_name = models.CharField(max_length=200, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    position = models.CharField(max_length=100, blank=True)
    team_name = models.CharField(max_length=200, blank=True)
    participants = models.TextField(
        blank=True, help_text="Enter one participant per line"
    )
    description = models.TextField()
    date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to="achievements/", blank=True, null=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-date", "-created_at"]

    def __str__(self):
        return self.title


class GeneralMemberApplication(models.Model):
    title = models.CharField(
        max_length=120,
        default="JOIN AS GENERAL MEMBER",
    )
    form_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = "General Member Application"
        verbose_name_plural = "General Member Application"

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    USER_TYPES = [
        ("admin", "Admin/Advisor"),
        ("member", "Member"),
        ("student", "Student"),
        ("guest", "Guest"),
    ]
    POSITION_CHOICES = [
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
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="userprofile"
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default="student")
    panel = models.ForeignKey(Panel, on_delete=models.SET_NULL, null=True, blank=True)
    student_id = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    is_bars_member = models.BooleanField(default=True)
    position_name = models.CharField(
        max_length=60,
        choices=POSITION_CHOICES,
        blank=True,
        null=True,
    )
    photo = models.ImageField(upload_to="users/photos/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.user_type}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Automatically make admin users staff and grant permissions
        if self.user_type == "admin":
            if not self.user.is_staff:
                self.user.is_staff = True
                self.user.save()
            
            # Grant all permissions for the 'VP' app
            from django.contrib.auth.models import Permission
            permissions = Permission.objects.filter(content_type__app_label='VP')
            self.user.user_permissions.set(permissions)
        else:
            # If not admin, ensure they are not staff (unless superuser) and clean up VP permissions
            if not self.user.is_superuser and self.user.is_staff:
                self.user.is_staff = False
                self.user.save()
                
                from django.contrib.auth.models import Permission
                permissions = Permission.objects.filter(content_type__app_label='VP')
                self.user.user_permissions.remove(*permissions)
