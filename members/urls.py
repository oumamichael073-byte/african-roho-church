from django.urls import path
from . import views
from . import utils

urlpatterns = [
    path('', views.member_list, name='member_list'),
    path('add/', views.add_member, name='add_member'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('attendance/', views.mark_attendance, name='mark_attendance'),
    path('tithe/add/', views.add_tithe, name='add_tithe'),
    path('offering/add/', views.add_offering, name='add_offering'),
    path('finance/', views.finance_dashboard, name='finance_dashboard'),
    path('events/add/', views.add_event, name='add_event'),
    path('reports/', views.reports, name='reports'),
    path('detail/<int:member_id>/', views.member_detail, name='member_detail'),
    path('edit/<int:member_id>/', views.edit_member, name='edit_member'),
    path('delete/<int:member_id>/', views.delete_member, name='delete_member'),
    path('reports/members/pdf/', utils.generate_member_pdf, name='members_pdf'),
    path('reports/finance/pdf/', utils.generate_finance_pdf, name='finance_pdf'),



]


