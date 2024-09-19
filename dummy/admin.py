from django.contrib import admin

from dummy.models import FirstDummy, SecondDummy


@admin.register(FirstDummy)
class FirstDummyAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'image',
    ]


@admin.register(SecondDummy)
class SecondDummyAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'file',
    ]
