# Generated by Django 3.0.5 on 2020-09-09 04:15

from django.db import migrations, models
import django.db.models.deletion
import django_mysql.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tasktpl', '0001_initial'),
        ('pipeline', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('params', django_mysql.models.JSONField(default=dict)),
                ('stage', models.IntegerField(default=1)),
                ('seq', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('pipeline', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task', to='pipeline.Pipeline')),
                ('tasktpl', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task', to='tasktpl.Tasktpl')),
            ],
            options={
                'db_table': 't_task',
            },
        ),
    ]
