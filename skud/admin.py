from django.contrib import admin
from skud.models import RawEvent, Employee, Department, EmployeeSummaryDay
from import_export.admin import ImportExportModelAdmin
from skud.resources import RawEventResource

class RawEventAdmin(ImportExportModelAdmin):
    resource_class = RawEventResource
    list_display = ('datetime','action_type','name','last_name','second_name','department',)
    search_fields = ('datetime','action_type','last_name','second_name','department',)

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name','first_name','last_name','department','day_start_datetime','day_end_datetime',)
    list_filter = ('department',)
    ordering = ('name','first_name','last_name',)
    search_fields = ('name','first_name','last_name','day_start_datetime','day_end_datetime',)

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)

class EmployeeSummaryDayAdmin(admin.ModelAdmin):
    list_display = ('date','employee','department','hours_delay','hours_way_out','hours_duration',)

admin.site.register(RawEvent, RawEventAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(EmployeeSummaryDay, EmployeeSummaryDayAdmin)