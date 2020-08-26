from django.contrib import admin
from .models import LiveTape, Statistic, LevelList, Payment, UserEvent, GameSession, PrizeWeight


class LiveTapeAdmin(admin.ModelAdmin):
    list_display = ['user', 'sum_win']

    class Meta:
        model = LiveTape


class StatisticAdmin(admin.ModelAdmin):
    list_display = ['name', 'value']

    class Meta:
        model = Statistic


class LevelListAdmin(admin.ModelAdmin):
    list_display = ['level', 'experience', 'reward']

    class Meta:
        model = LevelList


class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'sum_money', 'status', 'date']

    class Meta:
        model = Payment


class UserEventAdmin(admin.ModelAdmin):
    list_display = ['user', 'description', 'date']

    class Meta:
        model = UserEvent


class GameSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'case', 'sum_win']

    class Meta:
        model = GameSession


class PrizeWeightAdmin(admin.ModelAdmin):
    list_display = ['name', 'weights']

    class Meta:
        model = PrizeWeight


admin.site.register(LiveTape, LiveTapeAdmin)
admin.site.register(Statistic, StatisticAdmin)
admin.site.register(LevelList, LevelListAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(UserEvent, UserEventAdmin)
admin.site.register(GameSession, GameSessionAdmin)
admin.site.register(PrizeWeight, PrizeWeightAdmin)
