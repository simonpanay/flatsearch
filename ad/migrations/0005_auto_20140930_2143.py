# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ad', '0004_flatad_interesting'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='flatad',
            options={'ordering': ['interesting', '-pk']},
        ),
    ]
