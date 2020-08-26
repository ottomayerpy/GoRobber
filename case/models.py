from django.db import models


class Case(models.Model):
    """ Кейс для игры """
    name = models.CharField('Название', max_length=30)
    image = models.ImageField(verbose_name="Картинка", upload_to='cases/', height_field=None, width_field=None, max_length=100)
    image_cell = models.ImageField(verbose_name="Картинка ячейки", upload_to='cases/cells/', height_field=None, width_field=None, max_length=100)
    description = models.CharField('Описание', max_length=255)
    cost = models.IntegerField('Стоимость')
    level = models.IntegerField('Уровень')
    experience = models.IntegerField('Опыт')
    # Строго 12 элементов, так как на игровом поле только 12 ячеек
    prizes = models.TextField('Призы',
                              default='[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Кейс'
        verbose_name_plural = 'Кейсы'
