from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Nurse )
admin.site.register(Patient)
admin.site.register(Reservation)

'''
class usersAdmin(admin.ModelAdmin):
    search_fields = ['name']
    
    list_filter = ['name']
    

class nurseAdmin(admin.ModelAdmin):
   
    search_fields = ['name']
    list_filter = ['name']

admin.site.register(Nurse , nurseAdmin)
admin.site.register(Users , usersAdmin)
admin.site.register(Reservation)
'''