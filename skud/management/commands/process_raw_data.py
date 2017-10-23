# coding: utf-8
from django.core.management.base import BaseCommand
from skud.models import RawEvent, EmployeeSummaryDay, Employee, Department
from datetime import datetime, date

class Command(BaseCommand):

    def handle(self, *args, **options):

        self.controllers = self.get_controllers()
        self.action_types = self.get_action_types()

        self.raw_data = self.get_raw_data()
        print('===============================================')
        self.update_departments()
        self.update_employees()
        self.employees = Employee.objects.all()
        self.save_events()


    def get_controllers(self):
        controllers = {}
        for k, v in dict(RawEvent.CONTROLLER_CHOISES).items():
            controllers[v] = k
        return controllers


    def get_action_types(self):
        action_types = {}
        for k, v in dict(RawEvent.ACTION_TYPE_CHOICES).items():
            action_types[v] = k
        return action_types


    def get_max_date_entry(self):
        max_date_entry = None
        if EmployeeSummaryDay.objects.count() > 0:
            max_date_entry = EmployeeSummaryDay.objects.latest('date').date
            print('Max date entry ' + str(max_date_entry))
        print('Today ' + str(datetime.today()))
        return max_date_entry


    def get_raw_data(self):
        max_date_entry = self.get_max_date_entry()
        if max_date_entry:
            raw_data = RawEvent.objects.filter(datetime__range=[max_date_entry, datetime.today()],
                                               controller=self.controllers.get('Нижняя дверь'), name__isnull=False)
        else:
            raw_data = RawEvent.objects.filter(controller=self.controllers.get('Нижняя дверь'), name__isnull=False)

        return raw_data


    def update_departments(self):
        unique_departments = self.raw_data.filter().values("department").distinct()
        for department in unique_departments:
            department = department['department'].strip(' \t\n\r')
            if department.__len__() > 0:
                obj, created = Department.objects.update_or_create(
                    title=department,
                )
                obj.save()


    def update_employees(self):
        self.departments = Department.objects.all()
        unique_employees = self.raw_data.filter().values("name", "surname", "patronymic", "card_number", "department").distinct()
        for employee in unique_employees:

            if not employee['name']:
                continue

            try:
                department = self.departments.get(title=employee['department'])
            except:
                department = None

            obj, created = Employee.objects.update_or_create(
                name=employee['name'],
                surname=employee['surname'],
                patronymic=employee['patronymic'],
                department=department,
                card_number=employee['card_number'],
                defaults={'day_start_datetime': '10:00:00', 'day_end_datetime': '19:00:00'},
            )
            obj.save()


    def get_events_dict(self, raw_data):
        events = {}
        for event in raw_data:
            if not event.name or not event.datetime:
                continue

            fio = '{} {} {}'.format(event.name, event.surname, event.patronymic)

            if not events.get(fio):
                events[fio] = {}

            try:
                date = str(event.datetime.date())
            except:
                continue

            if not events[fio].get(date):
                events[fio][date] = []

            events[fio][date].append(event)

        return events


    def save_events(self):
        events_dict = self.get_events_dict(self.raw_data)
        for fio in events_dict:
            for date in events_dict[fio]:

                date_events = events_dict[fio][date]

                employee = self.employees.get(name=date_events[0].name, surname=date_events[0].surname,
                                                  patronymic=date_events[0].patronymic, card_number=date_events[0].card_number)
                if not employee:
                    continue

                date = date_events[0].datetime.date()
                department = self.departments.get(title=date_events[0].department)

                try:
                    date_events = self.sort_filter_date_events(date_events)
                except:
                    continue

                first_enter = self.calculate_first_enter(date_events)
                last_exit = self.calculate_last_exit(date_events)
                hours_delay = self.calculate_hours_delay(first_enter, employee)
                hours_way_out = self.calculate_hours_way_out(date_events, first_enter, last_exit)
                hours_duration = self.calculate_hours_duration(first_enter, last_exit)

                obj, created = EmployeeSummaryDay.objects.update_or_create(
                    date=date,
                    employee=employee,
                    department=department,
                )
                obj.first_enter = first_enter
                obj.last_exit = last_exit
                obj.hours_delay = hours_delay
                obj.hours_way_out = hours_way_out
                obj.hours_duration = hours_duration

                obj.save()

                print('Добавлена/Обновлена запись от {} на {}'.format(date, employee.name))

    # сортировка и фильтрация событий дня
    # по умолчанию: время по возрастанию
    def sort_filter_date_events(self, date_events):

        # тут может быть кастомная сортировка
        sorted_date_events = date_events

        # тут может быть кастомная фильтрация
        filtered_date_events = sorted_date_events

        if len(filtered_date_events) == 0:
            raise('Нет данных')

        return filtered_date_events

    # время первого входа в офис
    def calculate_first_enter(self, date_events):
        time = None

        for event in date_events:
            if event.action_type == self.action_types.get('Вход'):
                time = event.datetime.time()
                break

        return time

    # время последнего выхода из офиса
    def calculate_last_exit(self, date_events):
        time = None

        date_events.reverse()

        for event in date_events:
            if event.action_type == self.action_types.get('Выход'):
                time = event.datetime.time()
                break

        date_events.reverse()

        return time

    # Часы опоздания
    # Считаем: время первого входа минус время начала рабочего дня
    def calculate_hours_delay(self, first_enter, employee):

        if not first_enter or not employee.day_start_datetime:
            return None

        delta = (datetime.combine(date.min, first_enter) - datetime.combine(date.min, employee.day_start_datetime)).\
            total_seconds()

        if delta > 0:
            hours_delay = round(delta / 3600, 2)
        else:
            hours_delay = 0

        return hours_delay

    # часов вне офиса
    # считаем все выходы и входы, не учитывая первый вход и последний выход - всё, что по середине, грубо говоря
    def calculate_hours_way_out(self, date_events, first_enter, last_exit):

        if not first_enter or not last_exit:
            return None

        clear_date_events = []
        for event in date_events:
            # отсекаем всё, что до первого входа, включая первый вход
            if datetime.combine(date.min, event.datetime.time()) <= datetime.combine(date.min, first_enter):
                continue
            # отсекаем всё, что после последнего выхода, включая последний выход
            if datetime.combine(date.min, event.datetime.time()) >= datetime.combine(date.min, last_exit):
                continue
            clear_date_events.append(event)

        if len(clear_date_events) == 0:
            return None

        seconds_way_out = 0
        last_action_type = None
        last_time = None
        # находим пары выхода и входа, считаем время между ними и сохраняем значение
        for event in clear_date_events:
            if last_action_type == self.action_types.get('Выход') and event.action_type == self.action_types.get('Вход'):
                delta = (datetime.combine(date.min, event.datetime.time()) - datetime.combine(date.min, last_time)). \
                    total_seconds()
                seconds_way_out += delta

            last_action_type = event.action_type
            last_time = event.datetime.time()

        hours_way_out = round(seconds_way_out / 3600, 2)

        return hours_way_out

    # Часы между последним выходом и первым входом
    # Считаем: просто разница между этим временем
    def calculate_hours_duration(self, first_enter, last_exit):

        if not first_enter or not last_exit:
            return None

        delta = (datetime.combine(date.min, last_exit) - datetime.combine(date.min, first_enter)). \
            total_seconds()

        if delta > 0:
            hours_duration = round(delta / 3600, 2)
        else:
            hours_duration = 0

        return hours_duration
