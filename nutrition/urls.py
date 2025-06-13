from django.urls import path
from . import views

app_name = 'nutrition'

urlpatterns = [
    path('', views.recipe_list_view, name='recipe_list'), # Main recipe list
    path('categories/', views.nutrition_category_list_view, name='category_list'),
    path('category/<int:category_id>/', views.recipe_list_by_category_view, name='recipe_list_by_category'),
    path('recipe/<int:recipe_id>/', views.recipe_detail_view, name='recipe_detail'),
    path('recipe/add/', views.add_recipe_view, name='add_recipe'),
    path('recipe/<int:recipe_id>/edit/', views.edit_recipe_view, name='edit_recipe'),
    path('recipe/<int:recipe_id>/delete/', views.delete_recipe_view, name='delete_recipe'),
]
