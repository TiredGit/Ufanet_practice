from django.contrib import admin
from discounts_app import models


@admin.register(models.DiscountCategory)
class DiscountCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(models.Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('company_name',)


@admin.register(models.City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(models.DiscountCard)
class DiscountCardAdmin(admin.ModelAdmin):
    list_display = ('name', 'small_name', 'start_date', 'end_date')
