from django.http import JsonResponse

def placeholder(request):
    """Simple placeholder view for testing."""
    return JsonResponse({'status': 'ok', 'message': 'API is working'})
