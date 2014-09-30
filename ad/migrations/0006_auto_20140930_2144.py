# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ad', '0005_auto_20140930_2143'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='flatad',
            options={'ordering': ['-interesting', '-pk']},
        ),
    ]
