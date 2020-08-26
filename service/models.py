from django.db import models

from case.models import Case
from profile.models import UserProfile


class LiveTape(models.Model):
    """ Лайв лента сыгранных игр на главной """
    user = models.ForeignKey(UserProfile, verbose_name="Пользователь", on_delete=models.CASCADE)
    sum_win = models.IntegerField('Сумма выигрыша')

    def __str__(self):
        return self.user.user.username

    class Meta:
        verbose_name = 'Лайв лента'
        verbose_name_plural = 'Лайв лента'


class Statistic(models.Model):
    """ Статистика сайта """
    name = models.CharField('Название', max_length=255)
    value = models.IntegerField('Значение', default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Статистика'
        verbose_name_plural = 'Статистика'


class LevelList(models.Model):
    """ Уровни которые может прокачать пользователь """
    level = models.IntegerField('Уровень')
    experience = models.IntegerField('Опыт')
    reward = models.IntegerField('Вознаграждение')
    # Писать "no_description" если дополнительное описание не требуется
    additional_description = models.CharField('Дополнительное описание', max_length=255, default='no_description')

    def __str__(self):
        return f'Уровень {self.level} ({self.experience} XP)'

    class Meta:
        verbose_name = 'Уровень'
        verbose_name_plural = 'Уровни'


class Payment(models.Model):
    """ Финансовые операции """
    user = models.ForeignKey(UserProfile, verbose_name="Пользователь", on_delete=models.CASCADE)
    name = models.CharField('Название операции', max_length=255)
    sum_money = models.IntegerField('Сумма')
    status = models.CharField('Статус', max_length=255)
    date = models.DateTimeField('Дата', auto_now_add=True)

    def __str__(self):
        return self.user.user.username

    class Meta:
        verbose_name = 'Финансовая операция'
        verbose_name_plural = 'Финансовые операции'
        ordering = ['-date']


class UserEvent(models.Model):
    """ События пользователя """
    user = models.ForeignKey(UserProfile, verbose_name="Пользователь", on_delete=models.CASCADE)
    description = models.CharField('Описание', max_length=255)
    date = models.DateTimeField('Дата', auto_now_add=True)

    def __str__(self):
        return self.user.user.username

    class Meta:
        verbose_name = 'Событие пользователя'
        verbose_name_plural = 'События пользователей'


class GameSession(models.Model):
    """ Игровые сессии """
    user = models.ForeignKey(UserProfile, verbose_name="Пользователь", on_delete=models.CASCADE)
    case = models.ForeignKey(Case, verbose_name="Кейс", on_delete=models.CASCADE)
    sum_win = models.IntegerField('Сумма выигрыша', default=0)
    quantity_cells_available = models.IntegerField('Количество доступных ячеек')
    cells = models.TextField('Ячейки')
    unopened_cells = models.TextField('Не открытые ячейки')
    weight = models.TextField('Веса')

    def __str__(self):
        return self.user.user.username

    class Meta:
        verbose_name = 'Игровая сессия'
        verbose_name_plural = 'Игровые сессии'


class PrizeWeight(models.Model):
    """ Весá призов кейсов, для различных пользователей """
    name = models.CharField('Название', max_length=50, default='User')
    #  Порядковый номер вéса соответствует порядковому номеру приза в Case.prizes,
    #  чем больше вес тем больше вероятность выпадения это приза.
    #  Так как у кейса 12 призов то и весов 12
    weights = models.TextField('Веса', default='[1, 1, 1, 1, 1, 2, 2, 3, 3, 5, 5, 10]')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Веса призов кейса'
        verbose_name_plural = 'Веса призов кейсов'
