# Generated by Django 3.1.1 on 2020-09-17 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='JobPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jobTitle', models.CharField(max_length=150, null=True)),
                ('shortDescription', models.CharField(max_length=1000, null=True)),
                ('shortRequirement', models.CharField(max_length=1000, null=True)),
                ('link', models.CharField(max_length=150, null=True)),
            ],
        ),
    ]
