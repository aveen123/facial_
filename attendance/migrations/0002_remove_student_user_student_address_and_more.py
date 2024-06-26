# Generated by Django 5.0.3 on 2024-03-09 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='user',
        ),
        migrations.AddField(
            model_name='student',
            name='address',
            field=models.TextField(default='Unknown'),
        ),
        migrations.AddField(
            model_name='student',
            name='confirm_password',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='student',
            name='dob',
            field=models.DateField(default='2000-01-01'),
        ),
        migrations.AddField(
            model_name='student',
            name='emergency_contact_person',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='student',
            name='emergency_contact_phone',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='student',
            name='name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='student',
            name='password',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='student',
            name='personal_email',
            field=models.EmailField(default='', max_length=254),
        ),
        migrations.AddField(
            model_name='student',
            name='phone',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='student',
            name='picture',
            field=models.ImageField(default='default_picture.jpg', upload_to='student_pictures'),
        ),
        migrations.AddField(
            model_name='student',
            name='program',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='student',
            name='section',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='student',
            name='semester',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='student',
            name='student_id',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='student',
            name='username',
            field=models.CharField(default='', max_length=100),
        ),
    ]
