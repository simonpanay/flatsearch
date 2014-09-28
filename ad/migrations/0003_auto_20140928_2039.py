# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ad', '0002_auto_20140928_1620'),
    ]

    operations = [
        migrations.CreateModel(
            name='FlatImage',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('url', models.URLField(max_length=255)),
                ('ad', models.ForeignKey(to='ad.FlatAd')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='flatad',
            options={'ordering': ['-pk']},
        ),
        migrations.AlterField(
            model_name='flatad',
            name='energy_class',
            field=models.CharField(max_length=1, blank=True, choices=[('A', '<50'), ('B', '51 to 90'), ('C', '91 to 150'), ('D', '151 to 230'), ('E', '231 to 330'), ('F', '331 to 450'), ('G', '451 to 590'), ('H', '591 to 750'), ('I', '>750')]),
        ),
        migrations.AlterField(
            model_name='flatad',
            name='ges',
            field=models.CharField(max_length=1, blank=True, choices=[('A', '<5'), ('B', '6 to 10'), ('C', '11 to 20'), ('D', '21 to 35'), ('E', '36 to 55'), ('F', '56 to 80'), ('G', '81 to 110'), ('H', '110 to 145'), ('I', '>145')]),
        ),
    ]
