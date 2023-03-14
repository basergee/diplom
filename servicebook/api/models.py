from datetime import date

from django.db import models


class Handbook(models.Model):
    HANDBOOK_TYPES = (
        ('VM', 'Модель техники'),
        ('EM', 'Модель двигателя'),
        ('TM', 'Модель трансмиссии'),
        ('MA', 'Модель ведущего моста'),
        ('DA', 'Модель управляемого моста'),
        ('MT', 'Вид ТО'),
        ('FN', 'Узел отказа'),
        ('RD', 'Способ восстановления'),
        ('SC', 'Сервисная компания'),
    )

    # Название справочника. Например "модель техники"
    handbook_name = models.CharField(max_length=2, choices=HANDBOOK_TYPES)

    # Название элемента справочника
    title = models.CharField(max_length=200, unique=True)

    # Описание элемента справочника
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class Vehicle(models.Model):
    # Зав. № машины
    vehicle_id = models.CharField(max_length=20, unique=True,
                                  verbose_name='зав. № машины')

    # Модель техники
    vehicle_model = models.ForeignKey(Handbook, on_delete=models.CASCADE,
                                      verbose_name='Модель техники',
                                      related_name='vehicle_model')

    # Модель двигателя
    engine_model = models.ForeignKey(Handbook, on_delete=models.CASCADE,
                                     verbose_name='Модель двигателя',
                                     related_name='engine_model')

    # Зав. № двигателя
    engine_id = models.CharField(max_length=20,
                                 verbose_name='Зав. № двигателя')

    # Модель трансмиссии
    transmission_model = models.ForeignKey(Handbook, on_delete=models.CASCADE,
                                           verbose_name='Модель трансмиссии',
                                           related_name='transmission_model')

    # Зав. № трансмиссии
    transmission_id = models.CharField(max_length=20,
                                       verbose_name='Зав. № трансмиссии')

    # Модель ведущего моста
    main_axle_model = models.ForeignKey(Handbook, on_delete=models.CASCADE,
                                        verbose_name='Модель ведущего моста',
                                        related_name='main_axle_model')

    # Зав. № ведущего моста
    main_axle_id = models.CharField(max_length=20,
                                    verbose_name='Зав. № ведущего моста')

    # Модель управляемого моста
    driven_axle_model = models.ForeignKey(
        Handbook, on_delete=models.CASCADE,
        verbose_name='Модель управляемого моста',
        related_name='driven_axle_model')

    # Зав. № управляемого моста
    driven_axle_id = models.CharField(max_length=20,
                                      verbose_name='Зав. № управляемого моста')

    # Договор поставки №, дата
    contract_id_date = models.CharField(
        max_length=20, blank=True, verbose_name='Договор поставки №, дата')

    # Дата отгрузки с завода
    shipping_date = models.DateField(default=date.today,
                                     verbose_name='Дата отгрузки с завода')

    # Грузополучатель (конечный потребитель)
    consignee = models.CharField(
        max_length=100, verbose_name='Грузополучатель (конечный потребитель)')

    # Адрес поставки (эксплуатации)
    shipping_address = models.CharField(
        max_length=100, verbose_name='Адрес поставки (эксплуатации)')

    # Комплектация (доп. опции)
    equipment = models.TextField(verbose_name='Комплектация (доп. опции)',
                                 default='Стандарт')

    # Клиент
    client = models.CharField(max_length=100, verbose_name='Клиент')

    # Сервисная компания
    service_company = models.ForeignKey(Handbook, on_delete=models.CASCADE,
                                        verbose_name='Сервисная компания',
                                        related_name='service_company')

    def __str__(self):
        return self.vehicle_id


class Maintenance(models.Model):
    # Вид ТО
    maintenance_type = models.ForeignKey(
        Handbook, on_delete=models.CASCADE,
        verbose_name='Вид ТО',
        related_name='maintenance_type')

    # Дата проведения ТО
    maintenance_date = models.DateField(default=date.today,
                                        verbose_name='Дата проведения ТО')

    # Наработка, м/час
    operating_time = models.PositiveIntegerField(
        default=0, verbose_name='Наработка, м/час')

    # № заказ-наряда
    work_order_id = models.CharField(max_length=30,
                                     verbose_name='Номер заказ-наряда')

    # Дата заказ-наряда
    work_order_date = models.DateField(default=date.today,
                                       verbose_name='Дата заказ-наряда')

    # Зав. № машины
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE,
                                verbose_name='Машина')

    # Сервисная компания
    service_company = models.ForeignKey(Handbook, on_delete=models.CASCADE,
                                        verbose_name='Сервисная компания',
                                        related_name='maintenance_company')


class Reclamation(models.Model):
    # Дата отказа
    failure_date = models.DateField(default=date.today,
                                    verbose_name='Дата отказа')

    # Наработка, м/час
    operating_time = models.PositiveIntegerField(
        default=0, verbose_name='Наработка, м/час')

    # Узел отказа
    failure_node = models.ForeignKey(Handbook, on_delete=models.CASCADE,
                                     verbose_name='Узел отказа',
                                     related_name='failure_node')

    # Описание отказа
    failure_description = models.TextField(verbose_name='Описание отказа')

    # Способ восстановления
    repair_description = models.ForeignKey(
        Handbook, on_delete=models.CASCADE,
        verbose_name='Способ восстановления',
        related_name='repair_description')

    # Используемые запасные части
    spare_parts = models.TextField(blank=True,
                                   verbose_name='Используемые запасные части')

    # Дата восстановления
    repair_date = models.DateField(default=date.today,
                                   verbose_name='Дата восстановления')

    # Время простоя техники
    downtime = models.PositiveIntegerField(
        default=0, verbose_name='Время простоя техники')

    # Зав. № машины
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE,
                                verbose_name='Машина')

    # Сервисная компания
    service_company = models.ForeignKey(Handbook, on_delete=models.CASCADE,
                                        verbose_name='Сервисная компания',
                                        related_name='reclamation_company')
