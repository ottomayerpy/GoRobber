from django.contrib import admin
from django.contrib.sessions.models import Session
from django.contrib import admin
from .models import Case


class CaseAdmin(admin.ModelAdmin):
    list_display = ['name', 'cost', 'level', 'experience']

    class Meta:
        model = Case


admin.site.register(Case, CaseAdmin)
admin.site.register(Session)
