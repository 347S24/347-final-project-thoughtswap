# Generated by Django 4.2.11 on 2024-04-11 13:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0010_remove_facilitator_discussions'),
    ]

    operations = [
        migrations.AddField(
            model_name='thought',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='discussion.participant'),
        ),
    ]
