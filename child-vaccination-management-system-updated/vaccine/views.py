from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q, Count
from django.http import JsonResponse
from django.utils import timezone
from datetime import date, timedelta
from .models import Child, Vaccine, VaccinationSchedule, VaccinationRecord, Reminder
from .forms import ChildForm, VaccineForm, VaccinationScheduleForm, VaccinationRecordForm, ReminderForm, CustomUserCreationForm, CustomAuthenticationForm

def login_view(request):
    if request.user.is_authenticated:
        return redirect('vaccine:dashboard')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name}!')
                return redirect('vaccine:dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'vaccine/login.html', {'form': form})

def register_view(request):
    if request.user.is_authenticated:
        return redirect('vaccine:dashboard')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Admin account created successfully! Welcome, {user.first_name}!')
            login(request, user)
            return redirect('vaccine:dashboard')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'vaccine/register.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('vaccine:login')

def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            try:
                from django.contrib.auth.models import User
                user = User.objects.get(email=email)
                messages.success(request, f'Password reset instructions have been sent to {email}')
                return redirect('vaccine:login')
            except User.DoesNotExist:
                messages.error(request, 'No account found with this email address.')
        else:
            messages.error(request, 'Please enter your email address.')
    
    return render(request, 'vaccine/forgot_password.html')

@login_required
def dashboard(request):
    total_children = Child.objects.count()
    total_vaccines = Vaccine.objects.filter(is_active=True).count()
    scheduled_today = VaccinationSchedule.objects.filter(
        scheduled_date=date.today(),
        status='SCHEDULED'
    ).count()
    upcoming_vaccinations = VaccinationSchedule.objects.filter(
        scheduled_date__gte=date.today(),
        scheduled_date__lte=date.today() + timedelta(days=7),
        status='SCHEDULED'
    ).count()
    
    recent_records = VaccinationRecord.objects.select_related('child', 'vaccine').order_by('-administered_date')[:5]
    upcoming_schedules = VaccinationSchedule.objects.select_related('child', 'vaccine').filter(
        scheduled_date__gte=date.today(),
        status='SCHEDULED'
    ).order_by('scheduled_date')[:5]
    
    context = {
        'total_children': total_children,
        'total_vaccines': total_vaccines,
        'scheduled_today': scheduled_today,
        'upcoming_vaccinations': upcoming_vaccinations,
        'recent_records': recent_records,
        'upcoming_schedules': upcoming_schedules,
    }
    return render(request, 'vaccine/dashboard.html', context)

@login_required
def child_list(request):
    query = request.GET.get('q', '')
    children = Child.objects.all()
    
    if query:
        children = children.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(parent_name__icontains=query) |
            Q(parent_email__icontains=query)
        )
    
    context = {
        'children': children,
        'query': query,
    }
    return render(request, 'vaccine/child_list.html', context)

@login_required
def child_detail(request, pk):
    child = get_object_or_404(Child, pk=pk)
    schedules = VaccinationSchedule.objects.filter(child=child).select_related('vaccine').order_by('scheduled_date')
    records = VaccinationRecord.objects.filter(child=child).select_related('vaccine').order_by('-administered_date')
    
    context = {
        'child': child,
        'schedules': schedules,
        'records': records,
    }
    return render(request, 'vaccine/child_detail.html', context)

@login_required
def child_create(request):
    if request.method == 'POST':
        form = ChildForm(request.POST)
        if form.is_valid():
            child = form.save()
            messages.success(request, f'Child {child.first_name} {child.last_name} has been added successfully.')
            return redirect('vaccine:child_detail', pk=child.pk)
    else:
        form = ChildForm()
    
    return render(request, 'vaccine/child_form.html', {'form': form, 'title': 'Add New Child'})

@login_required
def child_update(request, pk):
    child = get_object_or_404(Child, pk=pk)
    if request.method == 'POST':
        form = ChildForm(request.POST, instance=child)
        if form.is_valid():
            child = form.save()
            messages.success(request, f'Child {child.first_name} {child.last_name} has been updated successfully.')
            return redirect('vaccine:child_detail', pk=child.pk)
    else:
        form = ChildForm(instance=child)
    
    return render(request, 'vaccine/child_form.html', {'form': form, 'title': 'Update Child', 'child': child})

@login_required
def child_delete(request, pk):
    child = get_object_or_404(Child, pk=pk)
    if request.method == 'POST':
        child.delete()
        messages.success(request, f'Child {child.first_name} {child.last_name} has been deleted successfully.')
        return redirect('vaccine:child_list')
    
    return render(request, 'vaccine/child_confirm_delete.html', {'child': child})

@login_required
def vaccine_list(request):
    query = request.GET.get('q', '')
    vaccines = Vaccine.objects.all()
    
    if query:
        vaccines = vaccines.filter(
            Q(name__icontains=query) |
            Q(manufacturer__icontains=query) |
            Q(description__icontains=query)
        )
    
    context = {
        'vaccines': vaccines,
        'query': query,
    }
    return render(request, 'vaccine/vaccine_list.html', context)

@login_required
def vaccine_detail(request, pk):
    vaccine = get_object_or_404(Vaccine, pk=pk)
    schedules = VaccinationSchedule.objects.filter(vaccine=vaccine).select_related('child').order_by('-scheduled_date')[:10]
    records = VaccinationRecord.objects.filter(vaccine=vaccine).select_related('child').order_by('-administered_date')[:10]
    
    context = {
        'vaccine': vaccine,
        'schedules': schedules,
        'records': records,
    }
    return render(request, 'vaccine/vaccine_detail.html', context)

@login_required
def vaccine_create(request):
    if request.method == 'POST':
        form = VaccineForm(request.POST)
        if form.is_valid():
            vaccine = form.save()
            messages.success(request, f'Vaccine {vaccine.name} has been added successfully.')
            return redirect('vaccine:vaccine_detail', pk=vaccine.pk)
    else:
        form = VaccineForm()
    
    return render(request, 'vaccine/vaccine_form.html', {'form': form, 'title': 'Add New Vaccine'})

@login_required
def vaccine_update(request, pk):
    vaccine = get_object_or_404(Vaccine, pk=pk)
    if request.method == 'POST':
        form = VaccineForm(request.POST, instance=vaccine)
        if form.is_valid():
            vaccine = form.save()
            messages.success(request, f'Vaccine {vaccine.name} has been updated successfully.')
            return redirect('vaccine:vaccine_detail', pk=vaccine.pk)
    else:
        form = VaccineForm(instance=vaccine)
    
    return render(request, 'vaccine/vaccine_form.html', {'form': form, 'title': 'Update Vaccine', 'vaccine': vaccine})

@login_required
def schedule_list(request):
    query = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')
    schedules = VaccinationSchedule.objects.select_related('child', 'vaccine').all()
    
    if query:
        schedules = schedules.filter(
            Q(child__first_name__icontains=query) |
            Q(child__last_name__icontains=query) |
            Q(vaccine__name__icontains=query)
        )
    
    if status_filter:
        schedules = schedules.filter(status=status_filter)
    
    schedules = schedules.order_by('scheduled_date')
    
    context = {
        'schedules': schedules,
        'query': query,
        'status_filter': status_filter,
        'status_choices': VaccinationSchedule.STATUS_CHOICES if hasattr(VaccinationSchedule, 'STATUS_CHOICES') else [
            ('SCHEDULED', 'Scheduled'),
            ('COMPLETED', 'Completed'),
            ('MISSED', 'Missed'),
            ('POSTPONED', 'Postponed'),
            ('CANCELLED', 'Cancelled'),
        ],
    }
    return render(request, 'vaccine/schedule_list.html', context)

@login_required
def schedule_create(request):
    if request.method == 'POST':
        form = VaccinationScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save()
            messages.success(request, f'Vaccination schedule for {schedule.child} has been created successfully.')
            return redirect('vaccine:schedule_list')
    else:
        form = VaccinationScheduleForm()
    
    return render(request, 'vaccine/schedule_form.html', {'form': form, 'title': 'Schedule Vaccination'})

@login_required
def schedule_update(request, pk):
    schedule = get_object_or_404(VaccinationSchedule, pk=pk)
    if request.method == 'POST':
        form = VaccinationScheduleForm(request.POST, instance=schedule)
        if form.is_valid():
            schedule = form.save()
            messages.success(request, f'Vaccination schedule for {schedule.child} has been updated successfully.')
            return redirect('vaccine:schedule_list')
    else:
        form = VaccinationScheduleForm(instance=schedule)
    
    return render(request, 'vaccine/schedule_form.html', {'form': form, 'title': 'Update Vaccination Schedule', 'schedule': schedule})

@login_required
def record_list(request):
    query = request.GET.get('q', '')
    records = VaccinationRecord.objects.select_related('child', 'vaccine').all()
    
    if query:
        records = records.filter(
            Q(child__first_name__icontains=query) |
            Q(child__last_name__icontains=query) |
            Q(vaccine__name__icontains=query) |
            Q(clinic_name__icontains=query)
        )
    
    records = records.order_by('-administered_date')
    
    context = {
        'records': records,
        'query': query,
    }
    return render(request, 'vaccine/record_list.html', context)

@login_required
def record_create(request):
    if request.method == 'POST':
        form = VaccinationRecordForm(request.POST)
        if form.is_valid():
            record = form.save()
            messages.success(request, f'Vaccination record for {record.child} has been created successfully.')
            return redirect('vaccine:record_list')
    else:
        form = VaccinationRecordForm()
    
    return render(request, 'vaccine/record_form.html', {'form': form, 'title': 'Add Vaccination Record'})

@login_required
def record_update(request, pk):
    record = get_object_or_404(VaccinationRecord, pk=pk)
    if request.method == 'POST':
        form = VaccinationRecordForm(request.POST, instance=record)
        if form.is_valid():
            record = form.save()
            messages.success(request, f'Vaccination record for {record.child} has been updated successfully.')
            return redirect('vaccine:record_list')
    else:
        form = VaccinationRecordForm(instance=record)
    
    return render(request, 'vaccine/record_form.html', {'form': form, 'title': 'Update Vaccination Record', 'record': record})

@login_required
def calendar_view(request):
    import calendar
    year = int(request.GET.get('year', date.today().year))
    month = int(request.GET.get('month', date.today().month))
    
    schedules = VaccinationSchedule.objects.filter(
        scheduled_date__year=year,
        scheduled_date__month=month
    ).select_related('child', 'vaccine')
    
    schedules_json = []
    for schedule in schedules:
        schedules_json.append({
            'id': schedule.id,
            'child_name': f"{schedule.child.first_name} {schedule.child.last_name}",
            'vaccine_name': schedule.vaccine.name,
            'scheduled_date': schedule.scheduled_date.strftime('%Y-%m-%d'),
            'status': schedule.status,
            'notes': schedule.notes
        })
    
    import json
    context = {
        'year': year,
        'month': month,
        'prev_month': month - 1 if month > 1 else 12,
        'next_month': month + 1 if month < 12 else 1,
        'prev_year': year if month > 1 else year - 1,
        'next_year': year if month < 12 else year + 1,
        'month_name': calendar.month_name[month],
        'schedules': schedules,
        'schedules_json': json.dumps(schedules_json),
    }
    return render(request, 'vaccine/calendar.html', context)

def search_api(request):
    query = request.GET.get('q', '')
    search_type = request.GET.get('type', 'all')
    
    results = {}
    
    if search_type in ['all', 'children']:
        children = Child.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(parent_name__icontains=query)
        )[:5]
        results['children'] = [{'id': c.id, 'name': f"{c.first_name} {c.last_name}", 'age': c.age} for c in children]
    
    if search_type in ['all', 'vaccines']:
        vaccines = Vaccine.objects.filter(
            Q(name__icontains=query) |
            Q(manufacturer__icontains=query)
        )[:5]
        results['vaccines'] = [{'id': v.id, 'name': v.name, 'manufacturer': v.manufacturer} for v in vaccines]
    
    return JsonResponse(results)