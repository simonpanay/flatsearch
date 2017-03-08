# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ad', '0011_auto_20170307_1957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='street',
            name='ad',
            field=models.OneToOneField(to='ad.FlatAd'),
        ),
    ]
