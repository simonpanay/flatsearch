# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ad', '0003_auto_20140928_2039'),
    ]

    operations = [
        migrations.AddField(
            model_name='flatad',
            name='interesting',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
