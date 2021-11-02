# Generated by Django 3.2.8 on 2021-11-01 06:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Interview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of each interview', max_length=100)),
                ('start_time', models.DateTimeField(help_text='Time when interview starts')),
                ('end_time', models.DateTimeField(help_text='Time when interview ends')),
                ('description', models.TextField(help_text='Interview description', max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(help_text='Question text', max_length=500)),
                ('type', models.CharField(choices=[('TA', 'Text answer'), ('OA', 'One answer'), ('MA', 'Many answers')], default='TA', help_text='Question type', max_length=2)),
                ('interview', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='InterviewerAPI_v2.interview')),
            ],
        ),
        migrations.CreateModel(
            name='PossibleAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='possible_answers', to='InterviewerAPI_v2.question')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text_answer', models.TextField(blank=True, null=True)),
                ('answer', models.ManyToManyField(blank=True, null=True, to='InterviewerAPI_v2.PossibleAnswer')),
                ('interview', models.ForeignKey(on_delete=models.SET('deleted'), to='InterviewerAPI_v2.interview')),
                ('question', models.ForeignKey(on_delete=models.SET('deleted'), to='InterviewerAPI_v2.question')),
                ('user', models.ForeignKey(help_text='Token of user', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
