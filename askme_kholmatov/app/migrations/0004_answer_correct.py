# Generated by Django 5.1.3 on 2024-11-14 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_rename_tag_question_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='correct',
            field=models.BooleanField(default=False),
        ),
    ]
