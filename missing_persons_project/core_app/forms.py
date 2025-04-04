from django import forms
from core_app.models import MissingPerson


class MissingPersonForm(forms.ModelForm):
    """
    Form for creating or updating a missing person record.
    """
    # Override fields to add widget attributes and remove labels
    full_name = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Full Name'
        })
    )
    
    age = forms.IntegerField(
        label='',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Age'
        })
    )
    
    last_seen_date = forms.DateTimeField(
        label='',
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'placeholder': 'mm/dd/yyyy --:--',
            'type': 'datetime-local'
        })
    )
    
    last_seen_location = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last Seen Location'
        })
    )
    
    contact_phone = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contact Phone Number'
        })
    )
    
    additional_info = forms.CharField(
        label='',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Additional Information',
            'rows': 4
        })
    )
    
    gender = forms.ChoiceField(
        label='',
        choices=[('', 'Gender')] + list(MissingPerson.GENDER_CHOICES),
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
    
    class Meta:
        model = MissingPerson
        fields = [
            'full_name', 'age', 'gender', 'last_seen_date', 
            'last_seen_location', 'contact_phone', 'additional_info'
        ]
        # Exclude photo field as requested 