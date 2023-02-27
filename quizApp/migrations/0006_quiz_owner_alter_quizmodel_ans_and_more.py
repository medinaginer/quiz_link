# Generated by Django 4.1.7 on 2023-02-20 19:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quizApp', '0005_alter_quizmodel_quiz'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='quizmodel',
            name='ans',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='quizmodel',
            name='option1',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='quizmodel',
            name='option2',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='quizmodel',
            name='option3',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='quizmodel',
            name='option4',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='quizmodel',
            name='question',
            field=models.CharField(max_length=250),
        ),
    ]