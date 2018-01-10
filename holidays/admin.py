from django.contrib import admin

from holidays.models import \
    CustomHoliday, NthXDayAfterHoliday, NthXDayHoliday, StaticHoliday

class StaticHolidayAdmin(admin.ModelAdmin):
    exclude = ('nth', 'day_of_week', 'after_nth', 'after_day_of_week', 'year',)
    readonly_fields = ('type',)

class NthXDayHolidayAdmin(admin.ModelAdmin):
    exclude = ('day', 'offset_weekend', 'after_nth', 'after_day_of_week', 'year',)
    readonly_fields = ('type',)

class NthXDayAfterHolidayAdmin(admin.ModelAdmin):
    exclude = ('day', 'offset_weekend', 'year',)
    readonly_fields = ('type',)

class CustomHolidayAdmin(admin.ModelAdmin):
    exclude = ('offset_weekend', 'nth', 'day_of_week', 'after_nth', 'after_day_of_week',)
    readonly_fields = ('type',)

admin.site.register(StaticHoliday, StaticHolidayAdmin)
admin.site.register(NthXDayHoliday, NthXDayHolidayAdmin)
admin.site.register(NthXDayAfterHoliday, NthXDayAfterHolidayAdmin)
admin.site.register(CustomHoliday, CustomHolidayAdmin)
