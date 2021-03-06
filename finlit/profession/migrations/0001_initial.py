# Generated by Django 3.2.5 on 2021-10-04 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prof_name', models.CharField(max_length=30)),
                ('prof_img', models.ImageField(upload_to='pics')),
                ('prof_desc', models.TextField()),
                ('income', models.BigIntegerField()),
                ('expend', models.BigIntegerField()),
                ('risk', models.IntegerField(choices=[(1, 'Low'), (2, 'Medium'), (3, 'High')])),
            ],
        ),
    ]
