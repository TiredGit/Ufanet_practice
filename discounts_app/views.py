from django.shortcuts import render
from django.views.generic import DetailView
from discounts_app import models

from django.shortcuts import render
from .models import DiscountCategory, DiscountCard

def categories_view(request):
    categories = DiscountCategory.objects.all()
    discounts = DiscountCard.objects.all()
    context = {
        'categories': categories,
        'discounts': discounts
    }
    return render(request, 'categories.html', context)