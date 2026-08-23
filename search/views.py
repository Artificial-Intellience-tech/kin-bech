from django.shortcuts import render
from django.db.models import Q
from accounts.models import User

def search_users(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        results = User.objects.filter(
            Q(username__icontains=query) | Q(email__icontains=query)
        )[:20]
    return render(request, 'search/search.html', {'query': query, 'results': results})