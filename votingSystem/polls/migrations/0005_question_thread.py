# Generated by Django 4.1.1 on 2024-12-01 15:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
        ('polls', '0004_alter_question_pub_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='thread',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='forum.thread'),
        ),
    ]
