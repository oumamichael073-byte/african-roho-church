from django.db import models

class Member(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    residence = models.CharField(max_length=200)

    join_date = models.DateField(auto_now_add=True)

    last_attendance = models.DateField(null=True, blank=True)
    photo = models.ImageField(
    upload_to='member_photos/',
    blank=True,
    null=True
)

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('transferred', 'Transferred'),
        ('deceased', 'Deceased'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active'
    )

    def __str__(self):
        return self.first_name + " " + self.last_name

class Attendance(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
    ]

    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.member.first_name} - {self.date} - {self.status}"
class Tithe(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.member.first_name} - {self.amount} - {self.date}"
class Offering(models.Model):
    description = models.CharField(max_length=200, default="Sunday Service Offering")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.description} - {self.amount}"
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    event_date = models.DateTimeField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title
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
