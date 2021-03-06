# Generated by Django 2.1.5 on 2019-01-30 08:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('cid', models.CharField(max_length=6, primary_key=True, serialize=False)),
                ('cflag', models.CharField(max_length=16)),
                ('sta', models.IntegerField()),
                ('tim', models.DateTimeField()),
                ('chetime', models.DateTimeField()),
                ('comtime', models.DateTimeField()),
                ('suretime', models.DateTimeField()),
                ('img', models.ImageField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Carord',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('stime', models.DateTimeField()),
                ('etime', models.DateTimeField()),
                ('foor', models.CharField(max_length=50)),
                ('drever', models.CharField(max_length=16)),
                ('time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Metorder',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('stime', models.DateTimeField()),
                ('etime', models.DateTimeField()),
                ('foor', models.CharField(max_length=50)),
                ('time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Metr',
            fields=[
                ('mid', models.CharField(max_length=6, primary_key=True, serialize=False)),
                ('size', models.IntegerField()),
                ('sta', models.IntegerField()),
                ('tim', models.DateTimeField()),
                ('lot', models.CharField(max_length=50)),
                ('dis', models.CharField(max_length=50)),
                ('img', models.ImageField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('acc', models.CharField(max_length=6, primary_key=True, serialize=False)),
                ('na', models.CharField(max_length=16)),
                ('paw', models.CharField(max_length=256)),
                ('sex', models.IntegerField()),
                ('offer', models.CharField(max_length=20)),
                ('part', models.CharField(max_length=16)),
                ('auth', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='metorder',
            name='acc',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sourcemanage.User'),
        ),
        migrations.AddField(
            model_name='metorder',
            name='mid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sourcemanage.Metr'),
        ),
        migrations.AddField(
            model_name='carord',
            name='acc',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sourcemanage.User'),
        ),
        migrations.AddField(
            model_name='carord',
            name='cid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sourcemanage.Car'),
        ),
    ]
