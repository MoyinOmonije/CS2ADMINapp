# Generated by Django 4.1.1 on 2022-09-27 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_rename_query_querytable_querydetails'),
    ]

    operations = [
        migrations.AddField(
            model_name='querytable',
            name='responseMessage',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='querytable',
            name='status',
            field=models.CharField(choices=[('responded', 'RESPONDED'), ('not responded', 'NOT RESPONDED')], default='not responded', max_length=20),
        ),
    ]
