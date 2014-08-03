from django.contrib import admin

from holidays.models import (Holiday, StaticHoliday, 
    NthXDayHoliday, NthXDayAfterHoliday, CustomHoliday)


class HolidayAdmin(admin.ModelAdmin):
    pass

class StaticHolidayAdmin(admin.ModelAdmin):
    pass

class NthXDayHolidayAdmin(admin.ModelAdmin):
    pass

class NthXDayAfterHolidayAdmin(admin.ModelAdmin):
    pass

class CustomHolidayAdmin(admin.ModelAdmin):
    pass

admin.site.register(Holiday, HolidayAdmin)
admin.site.register(StaticHoliday, StaticHolidayAdmin)
admin.site.register(NthXDayHoliday, NthXDayHolidayAdmin)
admin.site.register(NthXDayAfterHoliday, NthXDayAfterHolidayAdmin)
admin.site.register(CustomHoliday, CustomHolidayAdmin)
