from django.contrib import admin
from .models import Member, Attendance
from .models import Tithe
from .models import Offering
from .models import Event

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone', 'status', 'join_date')
    list_filter = ('status', 'join_date')
    search_fields = ('first_name', 'last_name', 'phone')


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('member', 'date', 'status')
    list_filter = ('status', 'date')

@admin.register(Tithe)
class TitheAdmin(admin.ModelAdmin):
    list_display = ('member', 'amount', 'date')
    list_filter = ('date',)
    search_fields = ('member__first_name', 'member__last_name')
@admin.register(Offering)
class OfferingAdmin(admin.ModelAdmin):
    list_display = ('description', 'amount', 'date')
    list_filter = ('date',)
    search_fields = ('description',)
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_date', 'location')
    list_filter = ('event_date',)
    search_fields = ('title', 'location')
