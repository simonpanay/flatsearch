# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ad', '0007_street'),
    ]

    operations = [
        migrations.AlterField(
            model_name='street',
            name='ad',
            field=models.ForeignKey(to='ad.FlatAd', unique=True),
        ),
    ]
