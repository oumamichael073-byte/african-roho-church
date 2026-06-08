from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='members_home'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path(
        'member/<int:member_id>/',
        views.member_profile,
        name='member_profile'
    ),

    path(
        'rankings/',
        views.member_rankings,
        name='member_rankings'
    ),

    path(
        'member/add/',
        views.add_member,
        name='add_member'
    ),

    path(
        'attendance/mark/',
        views.mark_attendance,
        name='mark_attendance'
    ),

    path(
        'finance/',
        views.finance_dashboard,
        name='finance_dashboard'
    ),

    path(
        'analytics/',
        views.analytics_dashboard,
        name='analytics_dashboard'
    ),

    path(
        'events/',
        views.event_list,
        name='event_list'
    ),

    path(
        'events/add/',
        views.add_event,
        name='add_event'
    ),

    path(
        'announcements/',
        views.announcement_list,
        name='announcement_list'
    ),

    path(
        'announcements/add/',
        views.add_announcement,
        name='add_announcement'
    ),

    path(
        'tithe/add/',
        views.add_tithe,
        name='add_tithe'
    ),

    path(
        'offering/add/',
        views.add_offering,
        name='add_offering'
    ),

    path(
        'leaders/',
        views.leader_list,
        name='leader_list'
    ),

    path(
        'leaders/add/',
        views.add_leader,
        name='add_leader'
    ),

    path(
        'financial-report/',
        views.financial_report,
        name='financial_report'
    ),

    path(
        'reports/members-pdf/',
        views.members_pdf,
        name='members_pdf'
    ),

    path(
        'prayer-request/',
        views.prayer_request,
        name='prayer_request'
    ),

    path(
        'prayer-success/',
        views.prayer_success,
        name='prayer_success'
    ),

    path(
        'gallery/',
        views.gallery,
        name='gallery'
    ),

    path(
        'sms/send/',
        views.send_sms,
        name='send_sms'
    ),
    path('members/', views.members_list, name='members_home'),
    path(
    'member/edit/<int:member_id>/',
    views.edit_member,
    name='edit_member'
    ),

    path(
    'member/delete/<int:member_id>/',
    views.delete_member,
    name='delete_member'
    ),
    
    path(
    'attendance/',
    views.attendance_list,
    name='attendance_list'
    ),
    
    path(
    'finance/giving/',
    views.member_giving_summary,
    name='member_giving'
    ),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path(
    'attendance/report/',
    views.attendance_report,
    name='attendance_report'
    ),
    
]
