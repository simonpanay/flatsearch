# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('ad', '0012_auto_20170308_0951'),
    ]

    operations = [
        migrations.AddField(
            model_name='flatad',
            name='last_updated',
            field=models.DateField(default=datetime.date(2017, 3, 10)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='flatad',
            name='published',
            field=models.DateField(default=datetime.date(2017, 3, 10)),
            preserve_default=False,
        ),
    ]
