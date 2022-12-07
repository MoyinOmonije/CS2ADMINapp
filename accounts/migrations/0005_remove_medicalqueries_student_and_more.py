# Generated by Django 4.1.1 on 2022-09-25 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0004_medicalqueries"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="medicalqueries",
            name="student",
        ),
        migrations.AddField(
            model_name="medicalqueries",
            name="studentNumber",
            field=models.CharField(default=1, max_length=10),
        ),
    ]