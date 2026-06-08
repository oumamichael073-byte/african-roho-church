from reportlab.pdfgen import canvas
from django.http import HttpResponse
from .models import Member, Tithe, Offering
from django.db.models import Sum


# -------------------------
# MEMBER REPORT PDF
# -------------------------
def generate_member_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="members_report.pdf"'

    p = canvas.Canvas(response)

def is_pastor(user):
    return user.groups.filter(
        name='Pastor'
    ).exists()


def is_treasurer(user):
    return user.groups.filter(
        name='Treasurer'
    ).exists()


def is_secretary(user):
    return user.groups.filter(
        name='Secretary'
    ).exists()


def is_admin(user):
    return user.groups.filter(
        name='Administrator'
    ).exists()
