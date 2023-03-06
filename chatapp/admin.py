from django.contrib import admin

from .models import Thread, Message

admin.site.register(Thread)
admin.site.register(Message)

admin.site.site_title = 'Admin panel DRF Chat'
admin.site.site_header = 'Admin panel DRF Chat'
