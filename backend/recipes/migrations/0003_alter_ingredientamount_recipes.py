# Generated by Django 3.2.7 on 2021-10-08 18:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_auto_20211008_2157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientamount',
            name='recipes',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe'),
        ),
    ]
