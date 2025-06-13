from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout # login needed if register redirects here
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomUserChangeForm, UserHealthDataForm
from .models import User, UserHealthData, Disease # Ensure User is imported
from .calculators import calculate_bmi, calculate_bmr_mifflin_st_jeor, calculate_daily_calorie_needs
from django.utils import timezone
from django.contrib.auth.views import LoginView as AuthLoginView
# from django.urls import reverse_lazy # if used

# ... (register_view, CustomLoginView, logout_view - assumed to be here from previous steps) ...
# For brevity, only redefining profile_view, profile_edit_view, health_data_add_view
# Ensure these are the only views in the file or adjust accordingly.

def register_view(request): # Copied from previous subtask output for completeness
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('users:profile')
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

class CustomLoginView(AuthLoginView): # Copied
    template_name = 'users/login.html'
login_view = CustomLoginView.as_view()

@login_required # Copied
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('users:login')


@login_required
def profile_view(request):
    user = request.user
    # Get the latest health data entry for display
    latest_health_data = UserHealthData.objects.filter(user=user).order_by('-date').first()
    all_health_data = UserHealthData.objects.filter(user=user).order_by('-date') # For graph later
    return render(request, 'users/profile.html', {
        'user': user,
        'latest_health_data': latest_health_data,
        'all_health_data': all_health_data
    })

@login_required
def profile_edit_view(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save() # User instance is updated here

            # Now, calculate and save/update UserHealthData
            bmi = None
            bmr = None
            calorie_target = None

            if user.weight_kg and user.height_cm:
                bmi = calculate_bmi(user.weight_kg, user.height_cm)

            if user.weight_kg and user.height_cm and user.age and user.sex:
                bmr = calculate_bmr_mifflin_st_jeor(user.weight_kg, user.height_cm, user.age, user.sex)

            if bmr and user.activity_level:
                calorie_target = calculate_daily_calorie_needs(bmr, user.activity_level)

            # Create or update a UserHealthData entry for today
            # This simple version creates a new entry each time profile is saved with relevant data.
            # A more complex version might update today's entry if it exists.
            if bmi is not None or bmr is not None or calorie_target is not None:
                UserHealthData.objects.update_or_create(
                    user=user,
                    date=timezone.now().date(),
                    defaults={
                        'weight_kg': user.weight_kg, # Store weight at time of calculation
                        'bmi': bmi,
                        'bmr': bmr,
                        'daily_calorie_target': calorie_target
                    }
                )
                messages.success(request, 'Profile updated and health metrics (BMI, BMR, Calories) calculated!')
            else:
                messages.success(request, 'Profile updated successfully!')
                if not (user.weight_kg and user.height_cm and user.age and user.sex and user.activity_level):
                    messages.warning(request, 'Health metrics (BMI, BMR, Calories) could not be calculated. Please ensure weight, height, age, sex, and activity level are set.')

            return redirect('users:profile')
        else:
            messages.error(request, 'Profile update failed. Please correct the errors below.')
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'users/profile_edit.html', {'form': form})

@login_required
def health_data_add_view(request): # Manual add view, might be less used now but keep
    if request.method == 'POST':
        form = UserHealthDataForm(request.POST)
        if form.is_valid():
            health_entry = form.save(commit=False)
            health_entry.user = request.user
            # Ensure date is included, form might not have it if not displayed
            if not health_entry.date:
                health_entry.date = timezone.now().date()
            health_entry.save()
            messages.success(request, 'Health data added successfully!')
            return redirect('users:profile')
        else:
            messages.error(request, 'Failed to add health data. Please correct the errors below.')
    else:
        form = UserHealthDataForm(initial={'date': timezone.now().date()})
    return render(request, 'users/health_data_form.html', {'form': form, 'view_title': 'Add/Update Health Data for Today'})
