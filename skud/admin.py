from django.contrib import admin
from skud.models import RawEvent, Employee, Department, EmployeeSummaryDay
from import_export.admin import ImportExportModelAdmin
from skud.resources import RawEventResource
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter

class RawEventAdmin(ImportExportModelAdmin):
    resource_class = RawEventResource
    list_display = ('datetime', 'action_type', 'controller', 'name', 'surname', 'patronymic', 'department',)
    search_fields = ('datetime', 'action_type', 'name', 'surname', 'patronymic', 'department',)
    list_filter = ('datetime', 'action_type', 'name', 'surname', 'patronymic', 'department',)

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'patronymic', 'department', 'card_number', 'day_start_datetime', 'day_end_datetime',)
    list_filter = ('department',)
    ordering = ('name', 'surname', 'patronymic',)
    search_fields = ('name', 'surname', 'patronymic', 'day_start_datetime', 'day_end_datetime',)

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)

class EmployeeSummaryDayAdmin(admin.ModelAdmin):
    change_list_template = 'admin/my_change_list.html'
    list_display = ('date', 'employee', 'department', 'first_enter', 'last_exit', 'hours_delay', 'hours_way_out', 'hours_duration',)
    list_filter = (('date', DateRangeFilter), ('employee', RelatedDropdownFilter), ('department', RelatedDropdownFilter),)
    search_fields = ('date', 'employee', 'department', 'first_enter', 'last_exit', 'hours_delay', 'hours_way_out', 'hours_duration',)
    readonly_fields = ('first_enter', 'last_exit', 'hours_delay', 'hours_way_out', 'hours_duration',)

    class Media:
        js = ('/static/admin/js/change_list_results.js',)

admin.site.register(RawEvent, RawEventAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(EmployeeSummaryDay, EmployeeSummaryDayAdmin)