from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_safe

# Create your views here.
@require_safe
def profile(request, username):
    person = get_object_or_404(get_user_model(), username=username)
    return render(request, 'acounts/profile.html', {'person':person})

