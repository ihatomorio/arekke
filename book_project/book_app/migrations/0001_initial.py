# Generated by Django 3.0.3 on 2020-03-07 07:43

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('author', models.CharField(max_length=256)),
                ('circle', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shop', models.IntegerField()),
                ('url', models.URLField(max_length=512)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('added_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book_app.Book')),
            ],
        ),
    ]
