from django.shortcuts import render, redirect
from .models import Member
from .forms import MemberForm
from .models import Attendance
from .forms import AttendanceForm
from datetime import date, timedelta
from .models import Tithe
from .forms import TitheForm
from .models import Offering
from .forms import OfferingForm
from .models import Event
from .forms import EventForm
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test

def is_pastor(user):
    return user.groups.filter(name='Pastor').exists() or user.is_superuser

def is_treasurer(user):
    return user.groups.filter(name='Treasurer').exists() or user.is_superuser

def is_teacher(user):
    return user.groups.filter(name='Teacher').exists() or user.is_superuser

def is_youth_leader(user):
    return user.groups.filter(name='Youth Leader').exists() or user.is_superuser

@login_required
def member_list(request):
    members = Member.objects.all().order_by('-join_date')
    return render(request, 'members/member_list.html', {'members': members})


def add_member(request):
    if request.method == 'POST':
        form = MemberForm(
    request.POST,
    request.FILES
)
        if form.is_valid():
            form.save()
            return redirect('member_list')
    else:
        form = MemberForm()

    return render(request, 'members/add_member.html', {'form': form})

def home(request):
    return render(request, 'members/home.html')

from django.db.models import Count
@login_required
def dashboard(request):
    total_members = Member.objects.count()
    active_members = Member.objects.filter(status='active').count()
    inactive_members = Member.objects.filter(status='inactive').count()

    total_tithes = Tithe.objects.aggregate(total=Sum('amount'))['total'] or 0
    total_offerings = Offering.objects.aggregate(total=Sum('amount'))['total'] or 0

    return render(request, 'members/dashboard.html', {
        'total_members': total_members,
        'active_members': active_members,
        'inactive_members': inactive_members,
        'total_tithes': total_tithes,
        'total_offerings': total_offerings,
    })
def mark_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            attendance = form.save()

            # update last attendance automatically
            member = attendance.member
            member.last_attendance = attendance.date
            member.save()

            return redirect('member_list')
    else:
        form = AttendanceForm()

    return render(request, 'members/attendance_form.html', {'form': form})
def update_inactive_members():
    ninety_days_ago = date.today() - timedelta(days=90)

    members = Member.objects.all()

    for member in members:
        if member.last_attendance:
            if member.last_attendance < ninety_days_ago:
                member.status = 'inactive'
                member.save()
        else:
            # if never attended at all
            member.status = 'inactive'
            member.save()
def add_tithe(request):
    if request.method == 'POST':
        form = TitheForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('member_list')
    else:
        form = TitheForm()

    return render(request, 'members/tithe_form.html', {'form': form})
def add_offering(request):
    if request.method == 'POST':
        form = OfferingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('member_list')
    else:
        form = OfferingForm()

    return render(request, 'members/offering_form.html', {'form': form})
from django.db.models import Sum
@login_required
@user_passes_test(is_treasurer)
def finance_dashboard(request):
    total_tithes = Tithe.objects.aggregate(total=Sum('amount'))['total'] or 0
    total_offerings = Offering.objects.aggregate(total=Sum('amount'))['total'] or 0

    total_income = total_tithes + total_offerings

    recent_tithes = Tithe.objects.order_by('-date')[:5]
    recent_offerings = Offering.objects.order_by('-date')[:5]

    context = {
        'total_tithes': total_tithes,
        'total_offerings': total_offerings,
        'total_income': total_income,
        'recent_tithes': recent_tithes,
        'recent_offerings': recent_offerings,
    }

    return render(request, 'members/finance_dashboard.html', context)
def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = EventForm()

    return render(request, 'members/event_form.html', {'form': form})
@login_required
@user_passes_test(is_pastor)
def reports(request):
    total_members = Member.objects.count()
    active_members = Member.objects.filter(status='active').count()
    inactive_members = Member.objects.filter(status='inactive').count()

    total_tithes = Tithe.objects.aggregate(total=Sum('amount'))['total'] or 0
    total_offerings = Offering.objects.aggregate(total=Sum('amount'))['total'] or 0

    context = {
        'total_members': total_members,
        'active_members': active_members,
        'inactive_members': inactive_members,
        'total_tithes': total_tithes,
        'total_offerings': total_offerings,
    }

    return render(request, 'members/reports.html', context)
def member_detail(request, member_id):
    member = get_object_or_404(Member, id=member_id)

    return render(
        request,
        'members/member_detail.html',
        {'member': member}
    )
def edit_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)

    if request.method == 'POST':
        form = MemberForm(request.POST, instance=member)

        if form.is_valid():
            form.save()
            return redirect('member_detail', member_id=member.id)

    else:
        form = MemberForm(instance=member)

    return render(
        request,
        'members/edit_member.html',
        {
            'form': form,
            'member': member
        }
    )
@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)

    if request.method == 'POST':
        member.delete()
        return redirect('member_list')

    return render(
        request,
        'members/delete_member.html',
        {'member': member}
    )
