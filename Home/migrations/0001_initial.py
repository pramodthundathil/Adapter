# Generated by Django 3.2.14 on 2023-03-22 08:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('User_Key', models.CharField(max_length=255)),
                ('User_Image', models.FileField(upload_to='profile_pic')),
                ('Hierachi_Level', models.IntegerField()),
                ('Sponser_income', models.FloatField(null=True)),
                ('Level_income', models.FloatField(null=True)),
                ('My_income', models.FloatField(null=True)),
                ('ReBirth_Income', models.FloatField(null=True)),
                ('UserId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
