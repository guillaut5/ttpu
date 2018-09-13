# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout




def logout_view(request):
    logout(request)
    # Redirect to a success page.
    
@login_required
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
# Create your views here.
