# Generated by Django 5.1 on 2024-09-09 17:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_remove_drone_base_remove_step_drone_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Obstacles',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('x_min', models.FloatField(null=True)),
                ('x_max', models.FloatField(null=True)),
                ('y_min', models.FloatField(null=True)),
                ('y_max', models.FloatField(null=True)),
                ('z_min', models.FloatField(null=True)),
                ('z_max', models.FloatField(null=True)),
                ('t_start', models.FloatField(null=True)),
                ('t_end', models.FloatField(null=True)),
                ('value', models.IntegerField(null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='bases',
            name='base_x_coordinate',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='bases',
            name='base_y_coordinate',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='bases',
            name='is_available',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='deliveries',
            name='drone',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.drones'),
        ),
        migrations.AlterField(
            model_name='deliveries',
            name='drop',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.droplocations'),
        ),
        migrations.AlterField(
            model_name='deliveries',
            name='pickup',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.pickuplocations'),
        ),
        migrations.AlterField(
            model_name='deliveries',
            name='requested_date',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='drones',
            name='base',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.bases'),
        ),
        migrations.AlterField(
            model_name='drones',
            name='battery_percentage',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='drones',
            name='drone_x_coordinate',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='drones',
            name='drone_y_coordinate',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='drones',
            name='drone_z_coordinate',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='drones',
            name='is_fault',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='drones',
            name='is_package_load',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='drones',
            name='is_package_unload',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='drones',
            name='last_communication',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='drones',
            name='planned_start_time',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='drones',
            name='ready_for_delivery',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='drones',
            name='step_index',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='drones',
            name='velocity',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='droplocations',
            name='drop_x_coordinate',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='droplocations',
            name='drop_y_coordinate',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='pickuplocations',
            name='pickup_x_coordinate',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='pickuplocations',
            name='pickup_y_coordinate',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='steps',
            name='drone',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.drones'),
        ),
        migrations.AlterField(
            model_name='steps',
            name='drone_x_coordinate',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='steps',
            name='drone_y_coordinate',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='steps',
            name='drone_z_coordinate',
            field=models.FloatField(null=True),
        ),
    ]
