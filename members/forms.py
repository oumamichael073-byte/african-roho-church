from django import forms
from .models import Member
from .models import Tithe
from .models import Offering
from .models import Event

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = [
            'first_name',
            'last_name',
            'phone',
            'email',
            'residence',
            'status',
            'photo',
        ]
from .models import Attendance

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['member', 'status']
class TitheForm(forms.ModelForm):
    class Meta:
        model = Tithe
        fields = ['member', 'amount']
class OfferingForm(forms.ModelForm):
    class Meta:
        model = Offering
        fields = ['description', 'amount']
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'location', 'event_date']

