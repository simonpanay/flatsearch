from django.contrib import admin

from .models import FlatAd

class FlatAdAdmin(admin.ModelAdmin):
    list_filter = (
        'ges',
        'energy_class',
        'rooms',
        'charges_included',
        'city',
    )

admin.site.register(FlatAd, FlatAdAdmin)
