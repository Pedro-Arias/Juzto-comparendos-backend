# Generated by Django 4.1.6 on 2023-08-09 15:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core_system', '0002_logmultas_multas'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComparendosHistory',
            fields=[
                ('id_comparendo', models.CharField(max_length=25, primary_key=True, serialize=False)),
                ('fotodeteccion', models.BooleanField(blank=True, null=True)),
                ('estado', models.CharField(blank=True, choices=[('1', 'Comparendo'), ('2', 'Resolución'), ('3', 'Cobro'), ('4', 'Archivado'), ('5', 'Inactivo')], max_length=11, null=True)),
                ('fecha_imposicion', models.DateField(blank=True, null=True)),
                ('fecha_resolucion', models.DateField(blank=True, null=True)),
                ('fecha_cobro_coactivo', models.DateField(blank=True, null=True)),
                ('numero_resolucion', models.CharField(blank=True, max_length=30, null=True)),
                ('numero_cobro_coactivo', models.CharField(blank=True, max_length=30, null=True)),
                ('placa', models.CharField(blank=True, max_length=6, null=True)),
                ('servicio_vehiculo', models.CharField(blank=True, choices=[('1', 'Particular'), ('2', 'Oficial'), ('3', 'Otros'), ('4', 'Publico'), ('5', 'No reportado'), ('6', 'Diplomatico')], max_length=12, null=True)),
                ('tipo_vehiculo', models.CharField(blank=True, choices=[('1', 'AUTOMOVIL'), ('2', 'MOTOCICLETA'), ('3', 'CAMION'), ('4', 'CAMIONETA'), ('5', 'BUSETA'), ('6', 'MICROBUS'), ('7', 'DESCONOCIDA'), ('8', 'CAMPERO'), ('9', 'TRACTO/CAMION')], max_length=13, null=True)),
                ('secretaria', models.CharField(blank=True, max_length=100, null=True)),
                ('direccion', models.CharField(blank=True, max_length=120, null=True)),
                ('valor_neto', models.FloatField(blank=True, null=True)),
                ('valor_pago', models.FloatField(blank=True, null=True)),
                ('scraper', models.CharField(blank=True, max_length=20, null=True)),
                ('fecha_notificacion', models.DateField(blank=True, null=True)),
                ('origen', models.CharField(blank=True, max_length=35, null=True)),
            ],
            options={
                'db_table': 'comparendos_history',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Logs_personas',
            fields=[
                ('id_logs_personas', models.OneToOneField(db_column='id_logs_personas', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='core_system.codigosconsulta')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('origen', models.CharField(max_length=15)),
                ('resultado', models.CharField(max_length=100)),
                ('data_lead', models.JSONField()),
            ],
            options={
                'db_table': 'logs_personas',
                'managed': False,
            },
        ),
    ]
