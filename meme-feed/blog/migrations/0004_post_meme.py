# Generated by Django 4.2.6 on 2023-10-24 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_rename_content_post_template_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='meme',
            field=models.URLField(default=''),
            preserve_default=False,
        ),
    ]
