from django.contrib import admin
from .models import Facilitator, Discussion, Student

# Register your models here.
admin.site.register(Facilitator)
admin.site.register(Discussion)


class FacilitatorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name')

    fields = ['first_last', 'last_name']

#admin.site.register(Facilitator, FacilitatorAdmin)
