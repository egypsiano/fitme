from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .forms import UserExerciseContributionForm
from users.models import User # Corrected import for User
from .models import Exercise, WorkoutCategory, Tag # Need User and Exercise for context

class UserExerciseContributionFormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='password123')
        category = WorkoutCategory.objects.create(name='Test Category')
        cls.exercise = Exercise.objects.create(name='Test Exercise', description='Desc', workout_category=category)

    def test_form_valid_with_image(self):
        # Minimal valid GIF
        image_data = b'GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;'
        image = SimpleUploadedFile("test_image.gif", image_data, content_type="image/gif")
        form_data = {'notes': 'Test notes'}
        file_data = {'uploaded_image': image}
        form = UserExerciseContributionForm(data=form_data, files=file_data)
        self.assertTrue(form.is_valid(), msg=form.errors.as_json())

    def test_form_valid_with_video_file(self):
        video = SimpleUploadedFile("test_video.mp4", b"file_content", content_type="video/mp4")
        form_data = {'notes': 'Test notes'}
        file_data = {'uploaded_video': video}
        form = UserExerciseContributionForm(data=form_data, files=file_data)
        self.assertTrue(form.is_valid())

    def test_form_valid_with_external_url(self):
        form_data = {'external_video_url': 'http://youtube.com/test', 'notes': 'Test notes'}
        form = UserExerciseContributionForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_if_no_media_provided(self):
        form_data = {'notes': 'Test notes'} # No image, video, or URL
        form = UserExerciseContributionForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors) # Check for non-field error related to clean method
        self.assertTrue('You must provide at least one contribution' in form.errors['__all__'][0])

from .models import Tag

class TagModelTests(TestCase):
    def test_tag_slug_auto_generation(self):
        tag = Tag.objects.create(name='Awesome Tag Example')
        self.assertEqual(tag.slug, 'awesome-tag-example')

    def test_tag_slug_is_preserved_if_provided(self):
        tag = Tag.objects.create(name='Another Tag', slug='custom-slug')
        self.assertEqual(tag.slug, 'custom-slug')

from django.urls import reverse

class WorkoutViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='workoutuser', password='password123')
        self.category = WorkoutCategory.objects.create(name='Strength')
        self.exercise = Exercise.objects.create(name='Push Up', description='Bodyweight exercise', workout_category=self.category)

    def test_category_list_view(self):
        response = self.client.get(reverse('workouts:category_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'workouts/category_list.html')

    def test_exercise_list_view(self):
        response = self.client.get(reverse('workouts:exercise_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'workouts/exercise_list.html')

    def test_exercise_detail_view(self):
        response = self.client.get(reverse('workouts:exercise_detail', args=[self.exercise.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'workouts/exercise_detail.html')

    def test_add_contribution_view_redirects_if_not_authenticated(self):
        response = self.client.get(reverse('workouts:add_exercise_contribution', args=[self.exercise.id]))
        self.assertEqual(response.status_code, 302)
