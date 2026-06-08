from django.contrib import admin
from .models import Member, Tithe, Offering, Attendance, Event, Announcement
from .models import Event
from .models import PrayerRequest
from .models import Gallery
from .models import SMSMessage

admin.site.register(Announcement)
admin.site.register(PrayerRequest)
admin.site.register(Gallery)
admin.site.register(SMSMessage)

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone', 'status')


@admin.register(Tithe)
class TitheAdmin(admin.ModelAdmin):
    list_display = ('member', 'amount', 'date')


@admin.register(Offering)
class OfferingAdmin(admin.ModelAdmin):
    list_display = ('member', 'amount', 'date')


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('member', 'service', 'date', 'status')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_date', 'location')
