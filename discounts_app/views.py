from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from discounts_app import models

from django.shortcuts import render
from .models import DiscountCategory, DiscountCard, City


def categories_view(request):
    categories = DiscountCategory.objects.all()
    cities = City.objects.all()
    selected_city_id = request.session.get('city_id')

    if selected_city_id:
        selected_city = City.objects.filter(id=selected_city_id).first()
    else:
        selected_city = City.objects.filter(name='Уфа').first()

    if 'city' in request.GET:
        try:
            selected_city = City.objects.get(id=request.GET.get('city'))
            request.session['city_id'] = selected_city.id
        except City.DoesNotExist:
            pass

    if selected_city:
        discounts = DiscountCard.objects.filter(cities=selected_city)
    else:
        discounts = DiscountCard.objects.all()

    selected_discount_id = request.GET.get('selected')
    selected_discount = None

    if selected_discount_id:
        try:
            selected_discount = DiscountCard.objects.get(id=selected_discount_id)
        except DiscountCard.DoesNotExist:
            pass

    for category in categories:
        if selected_city:
            category.city_offer_count = category.discount_cards.filter(cities=selected_city).count()
        else:
            category.city_offer_count = category.discount_cards.count()

    context = {
        'categories': categories,
        'discounts': discounts,
        'selected_discount': selected_discount,
        'cities': cities,
        'selected_city': selected_city
    }
    return render(request, 'categories.html', context)


def category_discounts_view(request, category_id):
    category = get_object_or_404(DiscountCategory, id=category_id)
    cities = City.objects.all()
    selected_city_id = request.session.get('city_id')

    if selected_city_id:
        selected_city = City.objects.filter(id=selected_city_id).first()
    else:
        selected_city = City.objects.filter(name='Уфа').first()
    discounts = DiscountCard.objects.filter(categories=category, cities=selected_city)

    selected_discount_id = request.GET.get('selected')
    selected_discount = None

    if selected_discount_id:
        try:
            selected_discount = DiscountCard.objects.get(id=selected_discount_id, categories=category)
        except DiscountCard.DoesNotExist:
            pass

    return render(request, 'discounts.html', {
        'category': category,
        'discounts': discounts,
        'selected_discount': selected_discount,
        'cities': cities
    })