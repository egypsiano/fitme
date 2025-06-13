from django.shortcuts import render, get_object_or_404, redirect
from .models import WorkoutCategory, Exercise, Tag, UserExerciseContribution, MuscleGroup
from .forms import ExerciseFilterForm, UserExerciseContributionForm
from django.db.models import Q # For complex queries
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.contrib import messages

def workout_category_list_view(request):
    categories = WorkoutCategory.objects.all().order_by('name')
    return render(request, 'workouts/category_list.html', {'categories': categories})

def exercise_list_view(request):
    exercises_qs = Exercise.objects.all().select_related('primary_muscle_group', 'workout_category').prefetch_related('equipment', 'tags', 'contraindicated_for_diseases')
    form = ExerciseFilterForm(request.GET or None)

    if form.is_valid():
        if form.cleaned_data.get('name'):
            exercises_qs = exercises_qs.filter(name__icontains=form.cleaned_data['name'])
        if form.cleaned_data.get('equipment'):
            exercises_qs = exercises_qs.filter(equipment__in=form.cleaned_data['equipment']).distinct()
        if form.cleaned_data.get('primary_muscle_group'):
            exercises_qs = exercises_qs.filter(primary_muscle_group=form.cleaned_data['primary_muscle_group'])
        if form.cleaned_data.get('difficulty'):
            exercises_qs = exercises_qs.filter(difficulty=form.cleaned_data['difficulty'])
        if form.cleaned_data.get('body_focus'):
            exercises_qs = exercises_qs.filter(body_focus=form.cleaned_data['body_focus'])
        if form.cleaned_data.get('is_home_friendly') is not None: # Check for True or False, not just truthy
            exercises_qs = exercises_qs.filter(is_home_friendly=form.cleaned_data['is_home_friendly'])
        if form.cleaned_data.get('tags'):
            exercises_qs = exercises_qs.filter(tags__in=form.cleaned_data['tags']).distinct()

    # Disease-based filtering for logged-in users
    if request.user.is_authenticated and hasattr(request.user, 'diseases') and request.user.diseases.exists():
        user_diseases = request.user.diseases.all()
        # Exclude exercises contraindicated for any of the user's diseases
        exercises_qs = exercises_qs.exclude(contraindicated_for_diseases__in=user_diseases)

    exercises = exercises_qs.order_by('name')

    return render(request, 'workouts/exercise_list.html', {
        'exercises': exercises,
        'list_title': 'All Exercises',
        'filter_form': form
    })

def exercise_list_by_category_view(request, category_id):
    category = get_object_or_404(WorkoutCategory, id=category_id)
    # This view could also use the filter form, but scoped to the category
    exercises = Exercise.objects.filter(workout_category=category).select_related('primary_muscle_group').prefetch_related('equipment', 'tags')

    # Basic disease filtering for this view too
    if request.user.is_authenticated and hasattr(request.user, 'diseases') and request.user.diseases.exists():
        user_diseases = request.user.diseases.all()
        exercises = exercises.exclude(contraindicated_for_diseases__in=user_diseases)

    exercises = exercises.order_by('name')

    return render(request, 'workouts/exercise_list.html', {
        'exercises': exercises,
        'category': category,
        'list_title': f'Exercises in {category.name}'
        # Could pass an empty form or a pre-filled one if adding filters here
    })

def exercise_detail_view(request, exercise_id):
    exercise = get_object_or_404(Exercise, id=exercise_id)
    # Check if this exercise is contraindicated for the user
    is_contraindicated = False
    if request.user.is_authenticated and hasattr(request.user, 'diseases'):
        user_diseases = request.user.diseases.all()
        if user_diseases.exists() and exercise.contraindicated_for_diseases.filter(id__in=user_diseases).exists():
            is_contraindicated = True

    return render(request, 'workouts/exercise_detail.html', {
        'exercise': exercise,
        'is_contraindicated': is_contraindicated
    })

@login_required
def add_exercise_contribution_view(request, exercise_id):
    exercise = get_object_or_404(Exercise, id=exercise_id)
    if request.method == 'POST':
        form = UserExerciseContributionForm(request.POST, request.FILES)
        if form.is_valid():
            contribution = form.save(commit=False)
            contribution.user = request.user
            contribution.exercise = exercise
            contribution.save()
            messages.success(request, f'Thank you! Your contribution for "{exercise.name}" has been submitted for review.')
            return redirect(reverse('workouts:exercise_detail', kwargs={'exercise_id': exercise.id}))
        else:
            messages.error(request, 'There was an error with your submission. Please check the form.')
    else:
        form = UserExerciseContributionForm()

    return render(request, 'workouts/add_exercise_contribution.html', {
        'form': form,
        'exercise': exercise
    })

@login_required
def list_user_contributions_view(request):
    contributions = UserExerciseContribution.objects.filter(user=request.user).select_related('exercise').order_by('-created_at')
    return render(request, 'workouts/list_user_contributions.html', {'contributions': contributions})

def interactive_muscle_map_view(request):
    # Fetch muscle groups marked to be shown on the map
    # Later, these could be split by front/back if the SVG requires it
    major_muscle_groups = MuscleGroup.objects.filter(show_on_map=True).order_by('name')

    # Placeholder for actual SVG file paths - these would be static files
    svg_front_url = None # settings.STATIC_URL + 'path/to/muscle_front.svg'
    svg_back_url = None  # settings.STATIC_URL + 'path/to/muscle_back.svg'

    # For now, we'll just pass the list of muscle groups to the template.
    # The template will list them, and clicking them will link to the filtered exercise list.

    return render(request, 'workouts/interactive_muscle_map.html', {
        'major_muscle_groups': major_muscle_groups,
        'svg_front_url': svg_front_url,
        'svg_back_url': svg_back_url,
        'filter_url_base': reverse_lazy('workouts:exercise_list') # Base URL for filtering
    })
