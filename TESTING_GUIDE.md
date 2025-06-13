# FitMe Application Testing Guide

This guide provides instructions on how to run automated tests and outlines key user flows for manual end-to-end testing.

## 1. Running Automated Tests

The project includes unit tests for backend logic (calculators, forms, models) and basic view tests.

**Prerequisites:**
*   Ensure you are in the project's root directory (where `manage.py` is located).
*   Have all dependencies from `requirements.txt` installed in your environment.

**Command to run tests:**

If running locally with a virtual environment:
```bash
python manage.py test
```

If using Docker Compose (ensure containers are built/running):
```bash
docker compose exec web python manage.py test
```

This command will discover and run all tests in files named `tests.py` within each application directory.

**Interpreting Output:**
*   Look for `OK` at the end, indicating all tests passed.
*   If tests fail, the output will show details about which tests failed and the reasons (e.g., assertion errors, exceptions).

## 2. Manual End-to-End (E2E) Testing - Key User Flows

Manual testing is crucial to ensure the application works as expected from a user's perspective. Test these flows in a browser, ideally after deploying to a staging or development environment.

**User Account Management:**
1.  **Registration:**
    *   Navigate to the registration page.
    *   Attempt to register with valid data. Verify successful registration and login.
    *   Attempt to register with invalid data (e.g., mismatched passwords, existing username). Verify error messages.
2.  **Login/Logout:**
    *   Log out if logged in.
    *   Navigate to the login page.
    *   Attempt login with invalid credentials. Verify error message.
    *   Log in with valid credentials. Verify successful login and redirection (e.g., to profile or dashboard).
    *   Log out. Verify successful logout.
3.  **Profile Update & Calculators:**
    *   Log in. Navigate to the profile edit page.
    *   Update personal details (weight, height, age, sex, activity level, diseases).
    *   Save changes. Verify profile page displays updated information.
    *   Check the Dashboard or Profile page: Verify that BMI, BMR, and Daily Calorie Needs are calculated/updated and displayed.
    *   Change weight again; verify historical data for weight chart is captured.

**Workout Functionality:**
1.  **View Workouts:**
    *   Navigate to the workout categories page. Verify categories (including Warm-up, Cool-down, Kegel if added by admin) are listed.
    *   Click a category. Verify exercises for that category are shown.
    *   Navigate to the 'All Exercises' list.
2.  **Filter Workouts:**
    *   On the 'All Exercises' page, use the filter form:
        *   Filter by equipment, muscle group, difficulty, body focus, home-friendly, tags. Verify results are accurate.
    *   If logged in with a user who has 'diseases' set, verify that exercises contraindicated for those diseases are excluded or flagged.
3.  **View Exercise Detail:**
    *   Click on an exercise. Verify all details (description, image, video link, instructions, etc.) are displayed correctly.
    *   If the exercise is contraindicated for the logged-in user, verify a warning is shown.
4.  **Interactive Muscle Map:**
    *   Navigate to the muscle map page.
    *   Click on a muscle group name. Verify redirection to the exercise list, filtered for that muscle.
5.  **User Exercise Contribution (as logged-in user):**
    *   Navigate to an exercise detail page.
    *   Click 'Add your own image/video'.
    *   Submit the contribution form (with an image, video file, or URL). Verify success message.
    *   Navigate to 'My Contributions'. Verify the submission is listed with 'Pending' status.
    *   (As Admin) Go to Django Admin -> User Exercise Contributions. Approve or Reject the submission.
    *   (As User) Refresh 'My Contributions'. Verify status is updated. If approved, check if it appears on the exercise detail page (Note: current implementation doesn't automatically display approved contributions on exercise detail, this could be a future enhancement).

**Nutrition Functionality:**
1.  **View Recipes:**
    *   Navigate to the nutrition categories page / recipe list page. Verify categories and recipes are listed.
    *   Filter recipes by category.
    *   Click on a recipe. Verify details are displayed.
2.  **Add/Edit/Delete Recipe (as logged-in user):**
    *   Click 'Add New Recipe'. Fill out the form (including image, video URL if applicable) and submit. Verify success and view the new recipe.
    *   Edit the created recipe. Verify changes are saved.
    *   Delete the created recipe. Verify it's removed from the list.

**Dashboard:**
1.  **View Dashboard (as logged-in user):**
    *   Navigate to the Dashboard.
    *   Verify personal summary and latest health metrics are displayed correctly.
    *   Verify the weight progress chart appears if sufficient data exists (at least 2 entries with weight). Add more health data via profile updates to test chart updates.

**Admin Section (as Admin user):**
1.  Log in to Django Admin.
2.  Navigate through various sections (Users, Workout Categories, Exercises, Tags, User Exercise Contributions, Nutrition Categories, Meal Recipes).
3.  Verify you can Add, View, Edit, and Delete items in each section.
4.  Specifically check moderation of User Exercise Contributions (approve/reject).

**Responsive Design:**
*   Using browser developer tools, switch to responsive/mobile view (e.g., iPhone, iPad dimensions).
*   Test all key user flows listed above.
*   Check for:
    *   Readable text.
    *   Properly sized tap targets (buttons, links).
    *   No horizontal scrolling.
    *   Hamburger menu functionality.
    *   Forms usability.
    *   Dashboard layout and chart responsiveness.

This manual testing checklist is not exhaustive but covers the main functionalities of FitMe.
