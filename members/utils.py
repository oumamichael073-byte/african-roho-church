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

    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, 800, "Church Members Report")

    y = 750

    members = Member.objects.all()

    for m in members:
        p.setFont("Helvetica", 10)
        p.drawString(50, y, f"{m.first_name} {m.last_name} - {m.phone} - {m.status}")
        y -= 20

        if y < 50:
            p.showPage()
            y = 800

    p.save()
    return response


# -------------------------
# FINANCIAL REPORT PDF
# -------------------------
def generate_finance_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="finance_report.pdf"'

    p = canvas.Canvas(response)

    tithes = Tithe.objects.aggregate(total=Sum('amount'))['total'] or 0
    offerings = Offering.objects.aggregate(total=Sum('amount'))['total'] or 0

    total_income = tithes + offerings

    p.setFont("Helvetica-Bold", 16)
    p.drawString(180, 800, "Church Financial Report")

    p.setFont("Helvetica", 12)
    p.drawString(50, 750, f"Total Tithes: {tithes}")
    p.drawString(50, 730, f"Total Offerings: {offerings}")
    p.drawString(50, 710, f"Total Income: {total_income}")

    p.save()
    return response

