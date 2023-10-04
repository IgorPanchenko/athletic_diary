from django.contrib import admin

from users.models import AdvUser

import datetime

from django.contrib import admin

from users.utilities import send_activation_notification




@admin.register(AdvUser)
class AdvUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name', 'phone_number', 'is_activated', 'date_joined')
    list_display_links = ('email',)
    list_editable = ('is_activated', )
    search_fields = ('phone_number', 'email', 'first_name', 'last_name')
    exclude = ['username']
    readonly_fields = ('last_login', 'date_joined')
    sortable_by = ['phone_number', 'id', 'email']
    list_filter = ['is_activated', ]
