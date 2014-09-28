# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FlatAd',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('city', models.CharField(choices=[('draft', 'draft'), ('published', 'published')], max_length=2)),
                ('zip_code', models.PositiveIntegerField()),
                ('price', models.PositiveIntegerField()),
                ('rooms', models.PositiveIntegerField()),
                ('charges_included', models.NullBooleanField()),
                ('flat_type', models.CharField(choices=[('flat', 'flat'), ('house', 'house')], max_length=1)),
                ('furnished', models.NullBooleanField()),
                ('area', models.PositiveIntegerField()),
                ('ges', models.CharField(choices=[('<5', '<5'), ('6 to 10', '6 to 10'), ('11 to 20', '11 to 20'), ('21 to 35', '21 to 35'), ('36 to 55', '36 to 55'), ('56 to 80', '56 to 80'), ('81 to 110', '81 to 110'), ('110 to 145', '110 to 145'), ('>145', '>145')], blank=True, max_length=1)),
                ('energy_class', models.CharField(choices=[('<50', '<50'), ('51 to 90', '51 to 90'), ('91 to 150', '91 to 150'), ('151 to 230', '151 to 230'), ('231 to 330', '231 to 330'), ('331 to 450', '331 to 450'), ('451 to 590', '451 to 590'), ('591 to 750', '591 to 750'), ('>750', '>750')], blank=True, max_length=1)),
                ('reviewed', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
