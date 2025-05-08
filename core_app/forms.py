from django import forms
from core_app.models import MissingPerson
from core_app.models import MissingPersonImage, RecordedVideo, LiveVideoSource


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

class MissingPersonImageForm(forms.ModelForm):
    """
    Form for uploading additional images of a missing person.
    """
    image = forms.ImageField(
        label='',
        widget=forms.FileInput(attrs={
            'class': 'form-control d-none',
            'accept': 'image/*',
            'data-action': 'image-upload'
        })
    )
    
    class Meta:
        model = MissingPersonImage
        fields = ['image']
        
class RecordedVideoForm(forms.ModelForm):
    """
    Form for uploading recorded videos for searching missing persons.
    """
    video = forms.FileField(
        label='',
        widget=forms.FileInput(attrs={
            'class': 'form-control d-none',
            'accept': 'video/*',
            'data-action': 'video-upload'
        })
    )
    
    class Meta:
        model = RecordedVideo
        fields = ['video']
        
class LiveVideoUrlForm(forms.ModelForm):
    """
    Form for adding a live video URL source.
    """
    url = forms.URLField(
        label='',
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'Live Stream URL'
        })
    )
    
    class Meta:
        model = LiveVideoSource
        fields = ['url']
        
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.source_type = 'url'
        if commit:
            instance.save()
        return instance
        
class LiveVideoWebcamForm(forms.ModelForm):
    """
    Form for setting up a webcam as a live video source.
    """
    class Meta:
        model = LiveVideoSource
        fields = []
        
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.source_type = 'webcam'
        # URL will be set by the view with the WebRTC connection details
        if commit:
            instance.save()
        return instance 