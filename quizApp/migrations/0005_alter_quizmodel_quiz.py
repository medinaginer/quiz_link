# Generated by Django 4.1.7 on 2023-02-19 11:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quizApp', '0004_alter_quizmodel_quiz'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizmodel',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='quizApp.quiz'),
        ),
    ]
