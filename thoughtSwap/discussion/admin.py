from django.contrib import admin
from .models import Facilitator, Discussion, Participant, Group, Thought, Prompt, Distribution, DistributedThought

# Register your models here.
admin.site.register(Facilitator)
admin.site.register(Discussion)
admin.site.register(Participant)
admin.site.register(Group)
admin.site.register(Thought)
admin.site.register(Distribution)
admin.site.register(DistributedThought)
admin.site.register(Prompt)


class FacilitatorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name')

    fields = ['first_last', 'last_name']


class DiscussionAdmin(admin.ModelAdmin):
    list_display = ('code', 'group')

    fields = ['code', 'group']

# admin.site.register(Facilitator, FacilitatorAdmin)
