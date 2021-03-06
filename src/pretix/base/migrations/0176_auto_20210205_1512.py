# Generated by Django 3.0.11 on 2021-02-05 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pretixbase', '0175_orderrefund_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventmetaproperty',
            name='allowed_values',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='eventmetaproperty',
            name='protected',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='eventmetaproperty',
            name='required',
            field=models.BooleanField(default=False),
        ),
    ]
