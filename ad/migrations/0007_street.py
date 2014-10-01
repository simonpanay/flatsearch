# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ad', '0006_auto_20140930_2144'),
    ]

    operations = [
        migrations.CreateModel(
            name='Street',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('street', models.CharField(max_length=255)),
                ('ad', models.ForeignKey(to='ad.FlatAd')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
