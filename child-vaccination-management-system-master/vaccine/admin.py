from django.contrib import admin
from .models import Child, Vaccine, VaccinationSchedule, VaccinationRecord, Reminder

@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'date_of_birth', 'gender', 'parent_name', 'parent_email', 'created_at']
    list_filter = ['gender', 'created_at', 'date_of_birth']
    search_fields = ['first_name', 'last_name', 'parent_name', 'parent_email']
    readonly_fields = ['age', 'created_at', 'updated_at']
    ordering = ['last_name', 'first_name']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'date_of_birth', 'gender', 'blood_group')
        }),
        ('Parent/Guardian Information', {
            'fields': ('parent_name', 'parent_phone', 'parent_email', 'emergency_contact')
        }),
        ('Address', {
            'fields': ('address',)
        }),
        ('Medical Information', {
            'fields': ('allergies', 'medical_conditions')
        }),
        ('System Information', {
            'fields': ('age', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Vaccine)
class VaccineAdmin(admin.ModelAdmin):
    list_display = ['name', 'manufacturer', 'recommended_age', 'dosage', 'is_active', 'created_at']
    list_filter = ['is_active', 'manufacturer', 'created_at']
    search_fields = ['name', 'manufacturer', 'description']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'manufacturer', 'is_active')
        }),
        ('Dosage Information', {
            'fields': ('recommended_age', 'dosage', 'route')
        }),
        ('Storage and Safety', {
            'fields': ('storage_requirements', 'side_effects', 'contraindications')
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(VaccinationSchedule)
class VaccinationScheduleAdmin(admin.ModelAdmin):
    list_display = ['child', 'vaccine', 'scheduled_date', 'status', 'created_at']
    list_filter = ['status', 'scheduled_date', 'vaccine', 'created_at']
    search_fields = ['child__first_name', 'child__last_name', 'vaccine__name']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['scheduled_date']
    
    fieldsets = (
        ('Schedule Information', {
            'fields': ('child', 'vaccine', 'scheduled_date', 'status')
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(VaccinationRecord)
class VaccinationRecordAdmin(admin.ModelAdmin):
    list_display = ['child', 'vaccine', 'administered_date', 'clinic_name', 'administering_healthcare_provider', 'created_at']
    list_filter = ['administered_date', 'vaccine', 'clinic_name', 'created_at']
    search_fields = ['child__first_name', 'child__last_name', 'vaccine__name', 'clinic_name', 'administering_healthcare_provider']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-administered_date']
    
    fieldsets = (
        ('Vaccination Information', {
            'fields': ('child', 'vaccine', 'administered_date', 'batch_number')
        }),
        ('Healthcare Provider', {
            'fields': ('administering_healthcare_provider', 'clinic_name')
        }),
        ('Medical Information', {
            'fields': ('next_dose_date', 'adverse_reactions', 'notes')
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ['child', 'vaccination_schedule', 'reminder_date', 'reminder_type', 'is_sent', 'created_at']
    list_filter = ['reminder_type', 'is_sent', 'reminder_date', 'created_at']
    search_fields = ['child__first_name', 'child__last_name', 'vaccination_schedule__vaccine__name']
    readonly_fields = ['created_at']
    ordering = ['reminder_date']
    
    fieldsets = (
        ('Reminder Information', {
            'fields': ('child', 'vaccination_schedule', 'reminder_date', 'reminder_type')
        }),
        ('Status', {
            'fields': ('is_sent', 'sent_at')
        }),
        ('System Information', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
