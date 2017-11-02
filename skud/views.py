from django.shortcuts import render_to_response, render
import datetime
from django.contrib.auth.decorators import login_required, permission_required

@login_required
def index(request):
    return render(
        request,
        'index.html',
        context={},
    )