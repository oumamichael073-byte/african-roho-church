from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Sum, Count
from .forms import MemberForm
from django.shortcuts import redirect
from django.utils.timezone import now
from datetime import timedelta
from django.utils import timezone
from .models import Leader
from .forms import LeaderForm
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from .models import PrayerRequest
from .forms import PrayerRequestForm
from .models import Gallery
from .models import SMSMessage, Member
from django.contrib.auth import authenticate, login, logout
from .models import Event

from .models import Member, Attendance, Tithe, Offering, Announcement, Event, Leader
from .utils import is_treasurer



# ---------------- DASHBOARD ----------------

from .models import Event


def dashboard(request):

    total_members = Member.objects.count()
    total_tithes = Tithe.objects.aggregate(total=Sum('amount'))['total'] or 0
    total_offerings = Offering.objects.aggregate(total=Sum('amount'))['total'] or 0
    total_attendance = Attendance.objects.count()

    # ✅ EVENTS (THIS IS THE IMPORTANT PART)
    upcoming_events = Event.objects.order_by('event_date')[:5]

    context = {
        "total_members": total_members,
        "total_tithes": total_tithes,
        "total_offerings": total_offerings,
        "total_attendance": total_attendance,

        # ✅ MUST BE HERE
        "upcoming_events": upcoming_events,
    }

    return render(request, "members/dashboard.html", context)


# ---------------- MEMBER PROFILE ----------------

@login_required
def member_profile(request, member_id):
    member = get_object_or_404(Member, id=member_id)

    attendance = Attendance.objects.filter(member=member)

    total_tithes = Tithe.objects.filter(member=member).aggregate(
        total=Sum("amount")
    )["total"] or 0

    total_offerings = Offering.objects.filter(member=member).aggregate(
        total=Sum("amount")
    )["total"] or 0

    context = {
        "member": member,
        "attendance": attendance,
        "total_tithes": total_tithes,
        "total_offerings": total_offerings,
    }

    return render(request, "members/member_profile.html", context)


# ---------------- MEMBER RANKINGS ----------------

from django.db.models import Count


def member_rankings(request):
    top_members = Member.objects.annotate(
        attendance_count=Count('attendance')
    ).order_by('-attendance_count')[:5]

    return render(request, "members/member_rankings.html", {
        "top_members": top_members
    })

@login_required
def add_member(request):

    if request.method == "POST":
        form = MemberForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("dashboard")

    else:
        form = MemberForm()

    return render(
        request,
        "members/add_member.html",
        {"form": form}
    )


def mark_attendance(request):

    members = Member.objects.all()

    if request.method == "POST":
        member_id = request.POST.get("member")
        status = request.POST.get("status")

        Attendance.objects.create(
            member_id=member_id,
            status=status
        )

        return redirect('attendance_list')

    return render(request, "members/mark_attendance.html", {
        "members": members
    })


from django.db.models import Sum

def finance_dashboard(request):

    total_tithes = Tithe.objects.aggregate(
        total=Sum('amount')
    )['total'] or 0

    total_offerings = Offering.objects.aggregate(
        total=Sum('amount')
    )['total'] or 0

    total_income = total_tithes + total_offerings

    recent_tithes = Tithe.objects.all().order_by('-id')[:5]
    recent_offerings = Offering.objects.all().order_by('-id')[:5]

    context = {
        "total_tithes": total_tithes,
        "total_offerings": total_offerings,
        "total_income": total_income,
        "recent_tithes": recent_tithes,
        "recent_offerings": recent_offerings,
    }

    return render(request, "members/finance_dashboard.html", context)

from django.db.models import Sum
from django.utils.timezone import now
from datetime import timedelta

from .models import Member, Tithe, Offering, Attendance


def analytics_dashboard(request):

    # TOTALS
    total_members = Member.objects.count()

    total_tithes = Tithe.objects.aggregate(
        total=Sum('amount')
    )['total'] or 0

    total_offerings = Offering.objects.aggregate(
        total=Sum('amount')
    )['total'] or 0

    total_attendance = Attendance.objects.count()

    # LAST 7 DAYS
    last_7_days = now().date() - timedelta(days=7)

    recent_attendance = Attendance.objects.filter(
        date__gte=last_7_days
    ).count()

    recent_tithes = Tithe.objects.filter(
        date__gte=last_7_days
    ).count()

    recent_offerings = Offering.objects.filter(
        date__gte=last_7_days
    ).count()

    context = {
        "total_members": total_members,
        "total_tithes": total_tithes,
        "total_offerings": total_offerings,
        "total_attendance": total_attendance,
        "recent_attendance": recent_attendance,
        "recent_tithes": recent_tithes,
        "recent_offerings": recent_offerings,
    }

    return render(request, "members/analytics_dashboard.html", context)


def event_list(request):
    events = Event.objects.order_by('-event_date')
    return render(request, "members/event_list.html", {"events": events})


from .models import Event

def add_event(request):

    if request.method == "POST":

        title = request.POST.get("title")
        event_date = request.POST.get("event_date")
        location = request.POST.get("location")

        Event.objects.create(
            title=title,
            event_date=event_date,
            location=location
        )

        return redirect('event_list')

    return render(request, "members/add_event.html")


def announcement_list(request):
    announcements = Announcement.objects.order_by('-created_at')
    return render(request, "members/announcement_list.html", {
        "announcements": announcements
    })

def add_announcement(request):
    if request.method == "POST":
        title = request.POST.get("title")
        message = request.POST.get("message")

        Announcement.objects.create(
            title=title,
            message=message
        )
        return redirect("announcement_list")

    return render(request, "members/add_announcement.html")


def add_tithe(request):
    members = Member.objects.all()

    if request.method == "POST":
        member_id = request.POST.get("member")
        amount = request.POST.get("amount")

        Tithe.objects.create(
            member_id=member_id,
            amount=amount
        )

        return redirect("dashboard")

    return render(request, "members/add_tithe.html", {"members": members})


def add_offering(request):
    members = Member.objects.all()

    if request.method == "POST":
        member_id = request.POST.get("member")
        amount = request.POST.get("amount")

        Offering.objects.create(
            member_id=member_id,
            amount=amount
        )

        return redirect("dashboard")

    return render(request, "members/add_offering.html", {"members": members})

def leader_list(request):
    leaders = Leader.objects.all()

    return render(
        request,
        "members/leader_list.html",
        {"leaders": leaders}
    )


def add_leader(request):
    if request.method == "POST":
        form = LeaderForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("leader_list")

    else:
        form = LeaderForm()

    return render(
        request,
        "members/add_leader.html",
        {"form": form}
    )

@login_required
@user_passes_test(is_treasurer)
def financial_report(request):

    total_tithes = Tithe.objects.aggregate(
        total=Sum("amount")
    )["total"] or 0

    total_offerings = Offering.objects.aggregate(
        total=Sum("amount")
    )["total"] or 0

    total_income = total_tithes + total_offerings

    members_giving = Member.objects.all()

    context = {
        "total_tithes": total_tithes,
        "total_offerings": total_offerings,
        "total_income": total_income,
        "members_giving": members_giving,
    }

    return render(
        request,
        "members/financial_report.html",
        context
    )


def members_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="members_report.pdf"'

    p = canvas.Canvas(response)

    members = Member.objects.all()

    y = 800
    p.setFont("Helvetica", 12)
    p.drawString(200, 820, "African Roho Msalaba Church Members Report")

    for m in members:
        p.drawString(50, y, f"{m.first_name} {m.last_name} - {m.phone}")
        y -= 20

        if y < 50:
            p.showPage()
            y = 800

    p.save()
    return response

def home(request):

    announcements = Announcement.objects.order_by(
        '-created_at'
    )[:5]

    events = Event.objects.order_by(
        'event_date'
    )[:5]

    leaders = Leader.objects.all()[:4]

    context = {
        "announcements": announcements,
        "events": events,
        "leaders": leaders,
    }

    return render(
        request,
        "members/home.html",
        context
    )


def prayer_request(request):

    if request.method == "POST":
        form = PrayerRequestForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("prayer_success")

    else:
        form = PrayerRequestForm()

    return render(
        request,
        "members/prayer_request.html",
        {"form": form}
    )


def prayer_success(request):
    return render(
        request,
        "members/prayer_success.html"
    )


def gallery(request):

    photos = Gallery.objects.order_by(
        '-uploaded_at'
    )

    return render(
        request,
        "members/gallery.html",
        {"photos": photos}
    )


from .models import SMSMessage
from django.shortcuts import render, redirect


def send_sms(request):

    if request.method == "POST":
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        SMSMessage.objects.create(
            phone=phone,
            message=message,
            status="sent"
        )

        return redirect('send_sms')

    messages = SMSMessage.objects.all().order_by('-id')[:10]

    return render(request, "members/send_sms.html", {
        "messages": messages
    })


def members_list(request):
    search = request.GET.get('search')

    members = Member.objects.all()

    if search:
        members = members.filter(first_name__icontains=search)

    return render(
        request,
        'members/members_list.html',
        {
            'members': members
        }
    )


def edit_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)

    if request.method == "POST":
        form = MemberForm(request.POST, request.FILES, instance=member)

        if form.is_valid():
            form.save()
            return redirect("members_home")
    else:
        form = MemberForm(instance=member)

    return render(request, "members/edit_member.html", {
        "form": form
    })


def delete_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)

    if request.method == "POST":
        member.delete()
        return redirect("members_home")

    return render(request, "members/delete_member.html", {
        "member": member
    })


def attendance_list(request):
    records = Attendance.objects.select_related('member').all().order_by('-id')

    return render(request, "members/attendance_list.html", {
        "records": records
    })


def member_giving_summary(request):
    members = Member.objects.all()

    for m in members:
        m.total_tithe = m.tithe_set.aggregate(total=Sum('amount'))['total'] or 0
        m.total_offering = m.offering_set.aggregate(total=Sum('amount'))['total'] or 0
        m.total_giving = m.total_tithe + m.total_offering

    return render(
        request,
        "members/member_giving.html",
        {"members": members}
    )


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("members_home")
        else:
            return render(request, "members/login.html", {
                "error": "Invalid username or password"
            })

    return render(request, "members/login.html")



def logout_view(request):
    logout(request)
    return redirect("login")


from django.utils.timezone import now
from datetime import timedelta

def attendance_report(request):
    today = now().date()

    last_7_days = today - timedelta(days=7)
    last_30_days = today - timedelta(days=30)

    weekly_attendance = Attendance.objects.filter(date__gte=last_7_days).count()
    monthly_attendance = Attendance.objects.filter(date__gte=last_30_days).count()

    total_attendance = Attendance.objects.count()

    context = {
        "weekly_attendance": weekly_attendance,
        "monthly_attendance": monthly_attendance,
        "total_attendance": total_attendance,
    }

    return render(request, "members/attendance_report.html", context)
