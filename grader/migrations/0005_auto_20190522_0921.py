# Generated by Django 2.1.4 on 2019-05-22 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grader', '0004_submission_complete'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lab',
            options={'ordering': ['-id']},
        ),
        migrations.AlterField(
            model_name='submission',
            name='output',
            field=models.CharField(max_length=1048576),
        ),
    ]
