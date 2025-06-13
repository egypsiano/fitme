from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, UserHealthData, Disease

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'sex', 'age', 'weight_kg', 'height_cm',) # Add diseases later via profile edit

class CustomUserChangeForm(forms.ModelForm): # Changed from UserChangeForm for more control
    diseases = forms.ModelMultipleChoiceField(
        queryset=Disease.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'sex', 'age', 'weight_kg', 'height_cm', 'diseases', 'activity_level')

class UserHealthDataForm(forms.ModelForm):
    class Meta:
        model = UserHealthData
        fields = ['date', 'weight_kg', 'bmi', 'bmr', 'daily_calorie_target']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
