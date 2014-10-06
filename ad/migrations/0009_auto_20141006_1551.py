# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ad', '0008_auto_20141001_1834'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flatad',
            name='city',
            field=models.CharField(max_length=255),
        ),
    ]
