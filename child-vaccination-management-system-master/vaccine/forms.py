from django import forms
from django.forms import DateInput, Textarea
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Child, Vaccine, VaccinationSchedule, VaccinationRecord, Reminder

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    terms_agreed = forms.BooleanField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name not in ['terms_agreed']:
                field.widget.attrs.update({'class': 'form-control'})
                # Set password fields to type password
                if field_name in ['password1', 'password2']:
                    field.widget.input_type = 'password'

class CustomAuthenticationForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

class ChildForm(forms.ModelForm):
    class Meta:
        model = Child
        fields = ['first_name', 'last_name', 'date_of_birth', 'gender', 'parent_name', 
                 'parent_phone', 'parent_email', 'address', 'emergency_contact', 
                 'blood_group', 'allergies', 'medical_conditions']
        widgets = {
            'date_of_birth': DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'parent_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1234567890'}),
            'parent_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'emergency_contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1234567890'}),
            'address': Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'allergies': Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'medical_conditions': Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name not in ['date_of_birth', 'gender', 'address', 'allergies', 'medical_conditions']:
                field.widget.attrs.update({'class': 'form-control'})

class VaccineForm(forms.ModelForm):
    class Meta:
        model = Vaccine
        fields = ['name', 'description', 'manufacturer', 'recommended_age', 'dosage', 
                 'route', 'storage_requirements', 'side_effects', 'contraindications', 'is_active']
        widgets = {
            'description': Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'storage_requirements': Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'side_effects': Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'contraindications': Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name not in ['description', 'storage_requirements', 'side_effects', 'contraindications']:
                field.widget.attrs.update({'class': 'form-control'})

class VaccinationScheduleForm(forms.ModelForm):
    class Meta:
        model = VaccinationSchedule
        fields = ['child', 'vaccine', 'scheduled_date', 'status', 'notes']
        widgets = {
            'scheduled_date': DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'notes': Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name not in ['scheduled_date', 'status', 'notes']:
                field.widget.attrs.update({'class': 'form-control'})

class VaccinationRecordForm(forms.ModelForm):
    class Meta:
        model = VaccinationRecord
        fields = ['child', 'vaccine', 'administered_date', 'batch_number', 
                 'administering_healthcare_provider', 'clinic_name', 'next_dose_date', 
                 'adverse_reactions', 'notes']
        widgets = {
            'administered_date': DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'next_dose_date': DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'adverse_reactions': Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'notes': Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name not in ['administered_date', 'next_dose_date', 'adverse_reactions', 'notes']:
                field.widget.attrs.update({'class': 'form-control'})

class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = ['child', 'vaccination_schedule', 'reminder_date', 'reminder_type']
        widgets = {
            'reminder_date': DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'reminder_type': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name not in ['reminder_date', 'reminder_type']:
                field.widget.attrs.update({'class': 'form-control'})
