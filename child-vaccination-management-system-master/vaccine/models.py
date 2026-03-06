from django.db import models
from django.utils import timezone
from datetime import date

class Child(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    parent_name = models.CharField(max_length=200)
    parent_phone = models.CharField(max_length=20)
    parent_email = models.EmailField()
    address = models.TextField()
    emergency_contact = models.CharField(max_length=20)
    blood_group = models.CharField(max_length=10, blank=True)
    allergies = models.TextField(blank=True)
    medical_conditions = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['last_name', 'first_name']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def age(self):
        today = date.today()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))

class Vaccine(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    manufacturer = models.CharField(max_length=100)
    recommended_age = models.CharField(max_length=50)  # e.g., "2 months", "6-8 weeks"
    dosage = models.CharField(max_length=50)
    route = models.CharField(max_length=50)  # e.g., "Intramuscular", "Oral"
    storage_requirements = models.TextField(blank=True)
    side_effects = models.TextField(blank=True)
    contraindications = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name

class VaccinationSchedule(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='vaccination_schedules')
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE, related_name='schedules')
    scheduled_date = models.DateField()
    status = models.CharField(max_length=20, choices=[
        ('SCHEDULED', 'Scheduled'),
        ('COMPLETED', 'Completed'),
        ('MISSED', 'Missed'),
        ('POSTPONED', 'Postponed'),
        ('CANCELLED', 'Cancelled'),
    ], default='SCHEDULED')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['scheduled_date']
        unique_together = ['child', 'vaccine', 'scheduled_date']
    
    def __str__(self):
        return f"{self.child} - {self.vaccine} on {self.scheduled_date}"

class VaccinationRecord(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='vaccination_records')
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE, related_name='records')
    administered_date = models.DateField()
    batch_number = models.CharField(max_length=50)
    administering_healthcare_provider = models.CharField(max_length=200)
    clinic_name = models.CharField(max_length=200)
    next_dose_date = models.DateField(null=True, blank=True)
    adverse_reactions = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-administered_date']
    
    def __str__(self):
        return f"{self.child} - {self.vaccine} on {self.administered_date}"

class Reminder(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='reminders')
    vaccination_schedule = models.ForeignKey(VaccinationSchedule, on_delete=models.CASCADE, related_name='reminders')
    reminder_date = models.DateField()
    reminder_type = models.CharField(max_length=20, choices=[
        ('EMAIL', 'Email'),
        ('SMS', 'SMS'),
        ('BOTH', 'Both'),
    ], default='EMAIL')
    is_sent = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['reminder_date']
    
    def __str__(self):
        return f"Reminder for {self.child} - {self.vaccination_schedule.vaccine} on {self.reminder_date}"
