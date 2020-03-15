# Generated by Django 3.0.4 on 2020-03-10 15:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('author', models.CharField(max_length=256)),
                ('circle', models.CharField(max_length=256)),
                ('shop', models.IntegerField(choices=[(0, 'なし'), (10, 'BOOTH'), (20, 'DLSite'), (31, 'FANZA電子書籍'), (40, 'FANZA同人'), (50, 'メロンブックス')])),
                ('url', models.URLField(max_length=512)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('added_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('image_path', models.ImageField(blank=True, upload_to='uploads/')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shop', models.IntegerField(choices=[(0, 'なし'), (10, 'BOOTH'), (20, 'DLSite'), (31, 'FANZA電子書籍'), (40, 'FANZA同人'), (50, 'メロンブックス')])),
                ('user', models.CharField(max_length=256)),
                ('password', models.CharField(max_length=256)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
