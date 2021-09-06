from django.contrib import admin
import trelloAPIs
from trelloAPIs.models import Cards, Comments, users, Lists, Projects
# Register your models here.
admin.site.register(Cards)
admin.site.register(Lists)
admin.site.register(Projects)
admin.site.register(users)
admin.site.register(Comments)