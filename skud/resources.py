from import_export import resources, fields, widgets
from skud.models import RawEvent

class RawEventResource(resources.ModelResource):

    datetime = fields.Field(column_name='Время',
                            attribute='datetime',
                            widget=widgets.DateTimeWidget(format='%d.%m.%Y %H:%M:%S'))
    controller = fields.Field(column_name='Контроллеры', attribute='controller')
    action_type = fields.Field(column_name='Вход и выход', attribute='action_type')
    card_number = fields.Field(column_name='Карта', attribute='card_number')
    status = fields.Field(column_name='Статус', attribute='status')
    surname = fields.Field(column_name='Фамилия', attribute='surname')
    name = fields.Field(column_name='Имя', attribute='name')
    patronymic = fields.Field(column_name='Отчество', attribute='patronymic')
    department = fields.Field(column_name='Отдел', attribute='department')

    def get_instance(self, instance_loader, row):
        # Returning False prevents us from looking in the
        # database for rows that already exist
        return False

    def skip_row(self, instance, original):
        events = RawEvent.objects.filter(datetime=instance.datetime,
                                         controller=instance.controller,
                                         card_number=instance.card_number)

        return True if events.count() > 0 else False

    class Meta:
        model = RawEvent
        skip_unchanged = True
        report_skipped = False
        fields = ('datetime', 'controller', 'action_type', 'card_number', 'status', 'surname', 'name', 'patronymic',
                  'department',)
        export_order = fields
