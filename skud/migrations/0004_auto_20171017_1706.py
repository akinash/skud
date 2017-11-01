# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-17 17:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('skud', '0003_auto_20171016_1504'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeesummaryday',
            name='first_enter',
            field=models.TimeField(blank=True, editable=False, null=True, verbose_name='Время первого входа'),
        ),
        migrations.AlterField(
            model_name='employeesummaryday',
            name='date',
            field=models.DateField(verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='employeesummaryday',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='skud.Department', verbose_name='Департамент'),
        ),
        migrations.AlterField(
            model_name='employeesummaryday',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='skud.Employee', verbose_name='Сотрудник'),
        ),
        migrations.AlterField(
            model_name='employeesummaryday',
            name='hours_delay',
            field=models.FloatField(blank=True, editable=False, null=True, verbose_name='Часов опоздания'),
        ),
        migrations.AlterField(
            model_name='employeesummaryday',
            name='hours_duration',
            field=models.FloatField(blank=True, editable=False, null=True, verbose_name='Часов от входа до выхода'),
        ),
        migrations.AlterField(
            model_name='employeesummaryday',
            name='hours_way_out',
            field=models.FloatField(blank=True, editable=False, null=True, verbose_name='Часов вне офиса'),
        ),
    ]