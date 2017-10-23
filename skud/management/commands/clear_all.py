# coding: utf-8
from django.core.management.base import BaseCommand
from skud.models import RawEvent, EmployeeSummaryDay, Employee, Department

class Command(BaseCommand):

    def handle(self, *args, **options):
        RawEvent.objects.all().delete()
        EmployeeSummaryDay.objects.all().delete()
        Employee.objects.all().delete()
        Department.objects.all().delete()