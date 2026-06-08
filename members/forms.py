from django import forms
from .models import Member, Event, Leader, PrayerRequest


# ---------------- MEMBER FORM ----------------
class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = '__all__'


# ---------------- EVENT FORM ----------------
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'


# ---------------- LEADER FORM ----------------
class LeaderForm(forms.ModelForm):
    class Meta:
        model = Leader
        fields = '__all__'


# ---------------- PRAYER REQUEST FORM ----------------
class PrayerRequestForm(forms.ModelForm):
    class Meta:
        model = PrayerRequest
        fields = ['name', 'phone', 'request']
