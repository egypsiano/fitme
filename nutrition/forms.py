from django import forms
from .models import MealRecipe

class MealRecipeForm(forms.ModelForm):
    class Meta:
        model = MealRecipe
        fields = ['name', 'description', 'ingredients', 'instructions',
                  'prep_time_minutes', 'cook_time_minutes', 'servings',
                  'category', 'image']
        widgets = {
            'ingredients': forms.Textarea(attrs={'rows': 5}),
            'instructions': forms.Textarea(attrs={'rows': 8}),
        }
        help_texts = {
            'image': 'Upload a picture of the finished meal.'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].required = True # Example: make category mandatory
