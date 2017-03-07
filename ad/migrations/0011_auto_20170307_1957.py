# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ad', '0010_auto_20141006_1554'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='flatad',
            options={'ordering': ['-interesting', 'reviewed', '-pk']},
        ),
    ]
