from django.db import models
from users.models import Disease # Import Disease from users app

class WorkoutCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'Workout Categories'

class Equipment(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name

class MuscleGroup(models.Model):
    show_on_map = models.BooleanField(default=False, help_text='Display this muscle group on the interactive map.')
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True, null=True) # Auto-generate from name if needed

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Exercise(models.Model):
    DIFFICULTY_CHOICES = [('BEG', 'Beginner'), ('INT', 'Intermediate'), ('ADV', 'Advanced')]
    BODY_FOCUS_CHOICES = [
        ('UPPER', 'Upper Body'),
        ('LOWER', 'Lower Body'),
        ('FULL', 'Full Body'),
        ('CORE', 'Core'),
        ('OTHER', 'Other'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    instructions = models.TextField(blank=True, null=True)
    representative_image = models.ImageField(upload_to='exercise_images/', null=True, blank=True, help_text='Admin uploaded representative image')
    video_url = models.URLField(blank=True, null=True, help_text='Link to external video (e.g., YouTube)')
    difficulty = models.CharField(max_length=3, choices=DIFFICULTY_CHOICES, default='INT')

    is_home_friendly = models.BooleanField(default=True, help_text='Can this exercise be typically done at home?')
    body_focus = models.CharField(max_length=5, choices=BODY_FOCUS_CHOICES, null=True, blank=True)

    workout_category = models.ForeignKey(WorkoutCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='exercises')
    primary_muscle_group = models.ForeignKey(MuscleGroup, on_delete=models.SET_NULL, null=True, blank=True, related_name='primary_exercises')

    equipment = models.ManyToManyField(Equipment, blank=True, related_name='exercises')
    secondary_muscle_groups = models.ManyToManyField(MuscleGroup, blank=True, related_name='secondary_exercises')
    tags = models.ManyToManyField(Tag, blank=True, related_name='exercises')
    contraindicated_for_diseases = models.ManyToManyField(
        Disease,
        blank=True,
        related_name='contraindicated_exercises',
        help_text='Select diseases for which this exercise is NOT recommended.'
    )

    def __str__(self):
        return self.name

class UserExerciseContribution(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending Approval'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='exercise_contributions')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='user_contributions')

    uploaded_image = models.ImageField(upload_to='user_exercise_contributions/images/', null=True, blank=True, help_text='Upload an image demonstrating the exercise.')
    uploaded_video = models.FileField(upload_to='user_exercise_contributions/videos/', null=True, blank=True, help_text='Upload a video demonstrating the exercise.')
    external_video_url = models.URLField(null=True, blank=True, help_text='Or, link to an external video (e.g., YouTube).')

    notes = models.TextField(blank=True, null=True, help_text='Any notes or comments about your contribution.')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} - {self.exercise.name} ({self.status})'

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'User Exercise Contributions'
