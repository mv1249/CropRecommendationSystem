# Generated by Django 3.1.5 on 2021-12-04 01:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CreateUser',
            fields=[
                ('sno', models.AutoField(primary_key=True, serialize=False)),
                ('fullname', models.CharField(max_length=50)),
                ('username', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
            ],
        ),
    ]
