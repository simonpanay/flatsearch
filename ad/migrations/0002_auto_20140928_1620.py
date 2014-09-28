# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ad', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flatad',
            name='city',
            field=models.CharField(choices=[('sm', "Saint-Martin-d'Hères"), ('gr', 'Grenoble')], max_length=2),
        ),
        migrations.AlterField(
            model_name='flatad',
            name='energy_class',
            field=models.CharField(choices=[('a', '<50'), ('b', '51 to 90'), ('c', '91 to 150'), ('d', '151 to 230'), ('e', '231 to 330'), ('f', '331 to 450'), ('g', '451 to 590'), ('h', '591 to 750'), ('i', '>750')], max_length=1, blank=True),
        ),
        migrations.AlterField(
            model_name='flatad',
            name='flat_type',
            field=models.CharField(choices=[('f', 'flat'), ('h', 'house')], max_length=1),
        ),
        migrations.AlterField(
            model_name='flatad',
            name='ges',
            field=models.CharField(choices=[('a', '<5'), ('b', '6 to 10'), ('c', '11 to 20'), ('d', '21 to 35'), ('e', '36 to 55'), ('f', '56 to 80'), ('g', '81 to 110'), ('h', '110 to 145'), ('i', '>145')], max_length=1, blank=True),
        ),
    ]
