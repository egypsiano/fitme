from django.contrib import admin
from .models import WorkoutCategory, Equipment, MuscleGroup, Exercise, Tag, UserExerciseContribution # Added UserExerciseContribution

class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('name', 'workout_category', 'primary_muscle_group', 'difficulty', 'is_home_friendly', 'body_focus', 'representative_image')
    list_filter = ('workout_category', 'primary_muscle_group', 'difficulty', 'is_home_friendly', 'body_focus', 'equipment', 'tags', 'contraindicated_for_diseases')
    search_fields = ('name', 'description')
    filter_horizontal = ('equipment', 'secondary_muscle_groups', 'tags', 'contraindicated_for_diseases')
    fieldsets = (
        (None, {'fields': ('name', 'description', 'instructions', 'representative_image', 'video_url')}),
        ('Categorization', {'fields': ('workout_category', 'primary_muscle_group', 'secondary_muscle_groups', 'tags')}),
        ('Details', {'fields': ('difficulty', 'is_home_friendly', 'body_focus', 'equipment')}),
        ('Health Considerations', {'fields': ('contraindicated_for_diseases',)}),
    )

class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)} # If not auto-generating in save method

admin.site.register(WorkoutCategory)
# admin.site.register(Equipment) # Replaced by EquipmentAdmin
# admin.site.register(MuscleGroup) # Replaced by MuscleGroupAdmin
admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(Tag, TagAdmin)

class EquipmentAdmin(admin.ModelAdmin):
    search_fields = ('name',)
admin.site.register(Equipment, EquipmentAdmin)

class MuscleGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'show_on_map')
    list_filter = ('show_on_map',)
    search_fields = ('name',)
admin.site.register(MuscleGroup, MuscleGroupAdmin)

class UserExerciseContributionAdmin(admin.ModelAdmin):
    list_display = ('user', 'exercise', 'status', 'created_at', 'uploaded_image', 'uploaded_video', 'external_video_url')
    list_filter = ('status', 'exercise', 'user')
    search_fields = ('user__username', 'exercise__name', 'notes')
    actions = ['approve_contributions', 'reject_contributions']
    readonly_fields = ('created_at', 'updated_at')

    def approve_contributions(self, request, queryset):
        queryset.update(status='APPROVED')
    approve_contributions.short_description = 'Mark selected contributions as Approved'

    def reject_contributions(self, request, queryset):
        queryset.update(status='REJECTED')
    reject_contributions.short_description = 'Mark selected contributions as Rejected'

admin.site.register(UserExerciseContribution, UserExerciseContributionAdmin)
