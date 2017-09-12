from django.db import models

class Department(models.Model):
    title = models.CharField(max_length = 100, verbose_name='Название')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Департамент"
        verbose_name_plural = "Департаменты"

class Employee(models.Model):
    name = models.CharField(max_length = 30, verbose_name='Имя', default=None)
    first_name = models.CharField(max_length = 30, blank=True, null=True, verbose_name='Фамилия')
    last_name = models.CharField(max_length = 30, blank=True, null=True, verbose_name='Отчество')
    department = models.ForeignKey(Department, blank=True, null=True, verbose_name='Департамент')
    day_start_datetime = models.TimeField(blank=True, null=True, verbose_name='Время начала рабочего дня')
    day_end_datetime = models.TimeField(blank=True, null=True, verbose_name='Время окончания рабочего дня')
    card_number = models.CharField(max_length=50, verbose_name='Номер карты', null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

class RawEvent(models.Model):

    ACTION_TYPE_CHOICES = (
        ('вход', 'Вход'),
        ('выход', 'Выход'),
    )

    CONTROLLER_CHOISES = (
        ('Z5R-Net 2k [40251]', 'Нижняя дверь'),
        ('Z5R-Net 2k [30964]', 'Верхняя дверь'),
    )

    datetime = models.DateTimeField(verbose_name='Время события')
    controller = models.CharField(max_length=20, choices=CONTROLLER_CHOISES, verbose_name='Контроллер')
    action_type = models.CharField(max_length=5, choices=ACTION_TYPE_CHOICES, verbose_name='Действие')
    card_number = models.CharField(max_length=100, verbose_name='Номер карты')
    status = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Фамилия')
    name = models.CharField(max_length=100, verbose_name='Имя')
    second_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Отчество')
    department = models.CharField(max_length=100, blank=True, null=True, verbose_name='Департамент')

    def __str__(self):
        return str(self.datetime)

    class Meta:
        verbose_name = 'Сырые данные: событие'
        verbose_name_plural = 'Сырые данные: события'

class EmployeeSummaryDay(models.Model):
    date = models.DateField()
    employee = models.ForeignKey(Employee)
    department = models.ForeignKey(Department, blank=True, null=True)
    hours_delay = models.FloatField(blank=True, null=True)
    hours_way_out = models.FloatField(blank=True, null=True)
    hours_duration = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.employee

    class Meta:
        verbose_name = "Summary по сотруднику за день"
        verbose_name_plural = "Summary по сотрудникам за день"

        
