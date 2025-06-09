from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from core_app.models import MissingPerson
from core_app.forms import MissingPersonForm

@login_required
def dashboard_view(request):
    """View for the main dashboard."""
    
    # Handle form submission
    if request.method == 'POST':
        # Check if we're editing an existing record
        profile_id = request.POST.get('profile_id')
        
        if profile_id:
            # Editing existing person
            instance = MissingPerson.objects.filter(id=profile_id, reported_by=request.user).first()
            if not instance:
                messages.error(request, "Missing person record not found or you don't have permission to edit it.")
                return redirect('core_app:dashboard')
                
            form = MissingPersonForm(request.POST, request.FILES, instance=instance)
        else:
            # Creating new person
            form = MissingPersonForm(request.POST, request.FILES)
        
        if form.is_valid():
            missing_person = form.save(commit=False)
            missing_person.reported_by = request.user
            missing_person.save()
            
            action = "updated" if profile_id else "created"
            messages.success(request, "Missing person record {} successfully.".format(action))
            return redirect('core_app:dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = MissingPersonForm()
    
    # Get user's reported missing persons for the saved profiles dropdown
    saved_profiles = MissingPerson.objects.filter(reported_by=request.user).order_by('-created_at')
    
    # Get basic statistics for dashboard
    total_missing_persons = MissingPerson.objects.filter(reported_by=request.user).count()
    # In the future, these would use the Search model
    successful_searches = 0
    failed_searches = 0
    active_searches = 0
    
    # Get recent search history (placeholder for now)
    # In the future, this would use the Search model
    search_history = []
    
    context = {
        'form': form,
        'saved_profiles': saved_profiles,
        'total_missing_persons': total_missing_persons,
        'successful_searches': successful_searches,
        'failed_searches': failed_searches,
        'active_searches': active_searches,
        'search_history': search_history
    }
    
    return render(request, 'core_app/dashboard.html', context) 