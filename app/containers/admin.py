from django.contrib import admin

# Register your models here.
from containers.models import *


admin.site.register(MainContainer)
admin.site.register(WebTrailerContainer)
admin.site.register(AppTrailerContainer)
admin.site.register(EventContainer)
admin.site.register(EventFooterContainer)