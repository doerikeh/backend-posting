# Generated by Django 3.0.5 on 2020-11-30 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kisahkita_art', '0006_posting_viewed'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('-date_created',)},
        ),
        migrations.AlterModelOptions(
            name='posting',
            options={'ordering': ('-date_created',)},
        ),
        migrations.AlterField(
            model_name='posting',
            name='viewed',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]