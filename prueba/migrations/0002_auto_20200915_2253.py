# Generated by Django 3.1.1 on 2020-09-15 22:53

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('prueba', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paciente',
            name='relacion_nucleo',
        ),
        migrations.AlterField(
            model_name='paciente',
            name='celular',
            field=models.CharField(blank=True, max_length=9, unique=True, validators=[django.core.validators.RegexValidator(message="El número debe ser del formato: '+XXXXXXXXX'. 9 digitos admitidos.", regex='^\\+?1?\\d{9,9}$')], verbose_name='Número de teléfono celular'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user_tipo',
            field=models.CharField(choices=[('DOCTOR', 'DOCTOR'), ('SECRETARIA', 'SECRETARIA'), ('PACIENTE', 'PACIENTE')], default='', max_length=15),
        ),
        migrations.CreateModel(
            name='Nucleo',
            fields=[
                ('matricula', models.CharField(blank=True, help_text='solo numeros', max_length=8, primary_key=True, serialize=False)),
                ('titular', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prueba.paciente')),
            ],
            options={
                'verbose_name': 'Nucleo',
                'verbose_name_plural': 'Nucleos',
            },
        ),
        migrations.CreateModel(
            name='Integrante',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('relacion_nucleo', models.CharField(choices=[('CONYUGE', 'CONYUGE'), ('MADRE', 'MADRE'), ('PADRE', 'PADRE'), ('HIJO', 'HIJO')], default='', max_length=12)),
                ('nucleo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prueba.nucleo')),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prueba.paciente')),
            ],
            options={
                'verbose_name': 'Integrante',
                'verbose_name_plural': 'Integrantes',
            },
        ),
        migrations.CreateModel(
            name='Foto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(auto_now_add=True, verbose_name='Fecha')),
                ('titulo', models.CharField(default='', max_length=125, verbose_name='Titulo')),
                ('contenido', models.TextField(default='', verbose_name='Contenido')),
                ('image', models.ImageField(upload_to='upload/imagenesConsulta', verbose_name='Imagen')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='foto_trat_doctor', to=settings.AUTH_USER_MODEL)),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prueba.paciente')),
            ],
            options={
                'db_table': 'ImgConsultas',
            },
        ),
        migrations.CreateModel(
            name='AntecedentesClinicos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fumador', models.CharField(choices=[('SI', 'SI'), ('NO', 'NO')], default='', max_length=2, verbose_name='Tabaco')),
                ('coproparasitario', models.CharField(choices=[('SI', 'SI'), ('NO', 'NO')], default='', max_length=2, verbose_name='Coproparasitario')),
                ('aparato_digestivo', models.CharField(choices=[('SI', 'SI'), ('NO', 'NO')], default='', max_length=2, verbose_name='Ap.Digestivo')),
                ('alergias', models.CharField(choices=[('SI', 'SI'), ('NO', 'NO')], default='', max_length=2, verbose_name='Alergias')),
                ('oncologicas', models.CharField(choices=[('SI', 'SI'), ('NO', 'NO')], default='', max_length=2, verbose_name='Oncologicas')),
                ('autoinmnunes', models.CharField(choices=[('SI', 'SI'), ('NO', 'NO')], default='', max_length=2, verbose_name='Autoinmunes')),
                ('intervenciones', models.CharField(choices=[('SI', 'SI'), ('NO', 'NO')], default='', max_length=2, verbose_name='Intervenciones')),
                ('endocrinometabólico', models.CharField(choices=[('DIABETES', 'DIABETES'), ('TIROIDES', 'TIROIDES'), ('DISPLEMIAS BAJO TRATAMIENTO', 'Infarto Agudo de Miocardio')], default='', max_length=27, verbose_name='Endocrinometabólico')),
                ('cardiovascular', models.CharField(choices=[('H.T.A.', 'HIPERTENSION'), ('ARRITMIAS', 'ARRITMIAS'), ('I.A.M', 'INFARTO MIOCARDIO'), ('OTROS', 'OTROS')], default='', max_length=27, verbose_name='Cardiovascular')),
                ('observations', models.TextField(verbose_name='Observaciones')),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prueba.paciente')),
            ],
        ),
    ]
