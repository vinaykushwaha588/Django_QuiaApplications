# Generated by Django 4.0.1 on 2022-05-06 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizapp', '0003_alter_questionmodel_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizcategory',
            name='image',
            field=models.ImageField(upload_to='media/category_image/'),
        ),
    ]
