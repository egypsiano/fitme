from django.urls import path
from . import views

app_name = 'workouts'

urlpatterns = [
    path('muscle-map/', views.interactive_muscle_map_view, name='interactive_muscle_map'),
    path('exercise/<int:exercise_id>/contribute/', views.add_exercise_contribution_view, name='add_exercise_contribution'),
    path('my-contributions/', views.list_user_contributions_view, name='list_user_contributions'),
    path('', views.workout_category_list_view, name='category_list'),
    path('exercises/', views.exercise_list_view, name='exercise_list'), # A general list for now
    path('category/<int:category_id>/', views.exercise_list_by_category_view, name='exercise_list_by_category'),
    path('exercise/<int:exercise_id>/', views.exercise_detail_view, name='exercise_detail'),
]
