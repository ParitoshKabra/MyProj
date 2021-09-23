# Generated by Django 3.2.6 on 2021-09-05 07:52

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cards',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=63)),
                ('descp', ckeditor.fields.RichTextField()),
                ('due_date', models.DateTimeField()),
                ('created_by', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('emailId', models.EmailField(max_length=254)),
                ('last_login', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Projects',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=63)),
                ('descp', ckeditor.fields.RichTextField()),
                ('created_by', models.IntegerField()),
                ('members', models.ManyToManyField(to='trelloAPIs.users')),
            ],
        ),
        migrations.CreateModel(
            name='Lists',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=63)),
                ('project_lists', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trelloAPIs.projects')),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_tym', models.DateTimeField()),
                ('comment', ckeditor.fields.RichTextField(default=None)),
                ('card_comments', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trelloAPIs.cards')),
                ('commented_by', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='trelloAPIs.users')),
            ],
        ),
        migrations.AddField(
            model_name='cards',
            name='assigned_to',
            field=models.ManyToManyField(to='trelloAPIs.users'),
        ),
        migrations.AddField(
            model_name='cards',
            name='cards_list',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trelloAPIs.lists'),
        ),
    ]