from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from .models import NutritionCategory, MealRecipe
from .forms import MealRecipeForm

def nutrition_category_list_view(request):
    categories = NutritionCategory.objects.all().order_by('name')
    return render(request, 'nutrition/category_list.html', {'categories': categories})

def recipe_list_view(request):
    recipes_qs = MealRecipe.objects.all().select_related('user', 'category')
    # Basic filtering by category (can be expanded with a form later)
    category_filter = request.GET.get('category')
    if category_filter:
        try: # Ensure category_filter is an integer
            category_filter = int(category_filter)
            recipes_qs = recipes_qs.filter(category__id=category_filter)
        except ValueError:
            category_filter = None # Invalid category ID, so ignore

    recipes = recipes_qs.order_by('-created_at')
    categories = NutritionCategory.objects.all().order_by('name') # For filter dropdown

    return render(request, 'nutrition/recipe_list.html', {
        'recipes': recipes,
        'categories': categories,
        'selected_category': category_filter,
        'list_title': 'All Meal Recipes'
    })

def recipe_list_by_category_view(request, category_id):
    category = get_object_or_404(NutritionCategory, id=category_id)
    recipes = MealRecipe.objects.filter(category=category).select_related('user').order_by('-created_at')
    return render(request, 'nutrition/recipe_list.html', {
        'recipes': recipes,
        'category': category,
        'list_title': f'Recipes in {category.name}'
    })

def recipe_detail_view(request, recipe_id):
    recipe = get_object_or_404(MealRecipe, id=recipe_id)
    return render(request, 'nutrition/recipe_detail.html', {'recipe': recipe})

@login_required
def add_recipe_view(request):
    if request.method == 'POST':
        form = MealRecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user
            recipe.save()
            messages.success(request, 'Your recipe has been added successfully!')
            return redirect(reverse_lazy('nutrition:recipe_detail', kwargs={'recipe_id': recipe.id}))
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = MealRecipeForm()
    return render(request, 'nutrition/recipe_form.html', {'form': form, 'form_title': 'Add a New Meal Recipe'})

@login_required
def edit_recipe_view(request, recipe_id):
    recipe = get_object_or_404(MealRecipe, id=recipe_id, user=request.user) # Ensure user owns the recipe
    if request.method == 'POST':
        form = MealRecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            messages.success(request, 'Recipe updated successfully!')
            return redirect(reverse_lazy('nutrition:recipe_detail', kwargs={'recipe_id': recipe.id}))
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = MealRecipeForm(instance=recipe)
    return render(request, 'nutrition/recipe_form.html', {'form': form, 'form_title': f'Edit Recipe: {recipe.name}'})

@login_required
def delete_recipe_view(request, recipe_id):
    recipe = get_object_or_404(MealRecipe, id=recipe_id, user=request.user) # Ensure user owns the recipe
    if request.method == 'POST':
        recipe.delete()
        messages.success(request, 'Recipe deleted successfully.')
        return redirect(reverse_lazy('nutrition:recipe_list'))
    return render(request, 'nutrition/recipe_confirm_delete.html', {'recipe': recipe})
