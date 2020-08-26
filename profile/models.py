from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """ Профиль пользователя """
    user = models.OneToOneField(User, verbose_name="Пользователь", on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', height_field=None, width_field=None, max_length=100, default='avatars/default_user_avatar.png')
    open_cases = models.IntegerField('Кол-во открытых кейсов', default=0)
    spent_money = models.IntegerField('Кол-во потраченых денег', default=0)
    balance = models.IntegerField('Баланс', default=1000)
    entered_money = models.IntegerField('Введено денег', default=0)
    withdraw_money = models.IntegerField('Выведено денег', default=0)
    level = models.IntegerField('Уровень', default=1)
    experience = models.IntegerField('Опыт', default=0)
    admin_mode = models.BooleanField('Админ мод', default=False)
    is_connection = models.BooleanField('Онлайн', default=False)
    quantity_connections = models.IntegerField('Количество открытых подключений', default=1)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """ Создает профиль пользователя после регистрации аккаунта """
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
