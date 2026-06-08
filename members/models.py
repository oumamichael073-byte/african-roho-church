from django.db import models


# ---------------- MEMBER ----------------
class Member(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField()
    residence = models.CharField(max_length=100)
    join_date = models.DateField(auto_now_add=True)
    last_attendance = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to='members/', null=True, blank=True)
    status = models.CharField(max_length=20, default='active')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# ---------------- TITHE ----------------
class Tithe(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.member} - {self.amount}"


# ---------------- OFFERING ----------------
class Offering(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.member} - {self.amount}"


# ---------------- ATTENDANCE ----------------
class Attendance(models.Model):
    SERVICE_CHOICES = [
        ('sunday', 'Sunday Service'),
        ('wednesday', 'Wednesday Service'),
        ('youth', 'Youth Service'),
    ]

    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
    ]

    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="attendance")
    service = models.CharField(max_length=20, choices=SERVICE_CHOICES)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    class Meta:
        unique_together = ('member', 'date', 'service')

    def __str__(self):
        return f"{self.member} - {self.service} - {self.status}"


# ---------------- ANNOUNCEMENT ----------------
class Announcement(models.Model):
    title = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# ---------------- EVENT ----------------
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    event_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# ---------------- LEADER ----------------
class Leader(models.Model):
    ROLE_CHOICES = [
        ('pastor', 'Pastor'),
        ('teacher', 'Teacher'),
        ('elder', 'Elder'),
        ('youth_leader', 'Youth Leader'),
    ]

    name = models.CharField(max_length=200)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=20, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.role}"


class PrayerRequest(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    request = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_prayed_for = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Gallery(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='gallery/')
    description = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class SMSMessage(models.Model):
    phone = models.CharField(max_length=20)
    message = models.TextField()
    status = models.CharField(max_length=20, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.phone
