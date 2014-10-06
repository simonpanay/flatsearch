# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def rename_city(apps, schema_editor):
    FlatAd = apps.get_model("ad", "FlatAd")
    for flat in FlatAd.objects.all():
        if flat.city == "sm":
            flat.city = "Saint-Martin-d'Hères"
            flat.save()
        elif flat.city == "gr":
            flat.city = "Grenoble"
            flat.save()


class Migration(migrations.Migration):

    dependencies = [
        ('ad', '0009_auto_20141006_1551'),
    ]

    operations = [
        migrations.RunPython(rename_city),
    ]
