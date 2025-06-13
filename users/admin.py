from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin # Renamed to avoid conflict
from .models import User, Disease, UserHealthData # Added UserHealthData

class UserHealthDataInline(admin.StackedInline):
    model = UserHealthData
    extra = 1 # Number of empty forms to display

class CustomUserAdmin(BaseUserAdmin):
    filter_horizontal = ('diseases', 'groups', 'user_permissions')
    inlines = [UserHealthDataInline]
    # To make custom fields visible in the main user change page:
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Custom Profile Data', {'fields': ('sex', 'age', 'weight_kg', 'height_cm', 'activity_level')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Custom Profile Data', {'fields': ('sex', 'age', 'weight_kg', 'height_cm', 'diseases', 'activity_level')}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(Disease)
admin.site.register(UserHealthData)
