from django import forms
from .models import Equipment, MuscleGroup, Tag, Exercise, UserExerciseContribution # Added UserExerciseContribution

class ExerciseFilterForm(forms.Form):
    name = forms.CharField(required=False, label='Exercise Name Contains')
    equipment = forms.ModelMultipleChoiceField(
        queryset=Equipment.objects.all().order_by('name'),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    primary_muscle_group = forms.ModelChoiceField(
        queryset=MuscleGroup.objects.all().order_by('name'),
        required=False,
        empty_label='Any Muscle Group'
    )
    difficulty = forms.ChoiceField(
        choices=[('', 'Any Difficulty')] + Exercise.DIFFICULTY_CHOICES,
        required=False
    )
    body_focus = forms.ChoiceField(
        choices=[('', 'Any Body Focus')] + Exercise.BODY_FOCUS_CHOICES,
        required=False
    )
    is_home_friendly = forms.NullBooleanField( # Allows 'Any', 'Yes', 'No'
        required=False,
        widget=forms.Select(choices=[(None, 'Any'), (True, 'Yes'), (False, 'No')])
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all().order_by('name'),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    # Add other filters as needed, e.g., category
    # workout_category = forms.ModelChoiceField(queryset=WorkoutCategory.objects.all(), required=False)

class UserExerciseContributionForm(forms.ModelForm):
    class Meta:
        model = UserExerciseContribution
        fields = ['uploaded_image', 'uploaded_video', 'external_video_url', 'notes']
        help_texts = {
            'uploaded_image': 'Optional. Upload an image.',
            'uploaded_video': 'Optional. Upload a video file.',
            'external_video_url': 'Optional. Provide a link to a video (e.g., YouTube, Vimeo).',
            'notes': 'Optional. Add any comments about your submission.',
        }

    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get('uploaded_image')
        video_file = cleaned_data.get('uploaded_video')
        video_url = cleaned_data.get('external_video_url')

        if not image and not video_file and not video_url:
            raise forms.ValidationError('You must provide at least one contribution: an image, a video file, or an external video link.')
        return cleaned_data
