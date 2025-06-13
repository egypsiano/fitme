# FitMe Administrator Guide

This guide provides instructions for administrators to manage the FitMe website content and users.

## 1. Introduction
As an administrator, you have full control over the content on FitMe, including managing users, workout definitions, nutrition recipes, and moderating user-submitted content.

## 2. Accessing the Admin Panel
1.  Navigate to the admin URL, typically `yourdomain.com/admin/`.
2.  Log in using your administrator credentials.

## 3. User Management
*   In the admin panel, go to **Users > Users**.
*   Here you can:
    *   **View** all registered users.
    *   **Add** new users manually (though registration is usually user-driven).
    *   **Edit** user details: Click on a username. You can change their profile information, activity level, assigned diseases, and permissions (e.g., staff status, superuser status, group memberships).
    *   **Delete** users.
*   **Diseases:** Manage the list of available diseases under **Users > Diseases**.
*   **User Health Data:** View user-specific health data entries under **Users > User Health Data** (usually for reference, as this is auto-generated).

## 4. Workout Content Management

### Managing Workout Categories
*   Go to **Workouts > Workout Categories**.
*   Here you can Add, Edit, or Delete categories like 'Arms', 'Chest', 'Legs'.
*   **Warm-up, Cool-down, Kegel Exercises:** These are also managed as Workout Categories. Ensure categories like 'Warm-up Exercises', 'Cool-down Exercises', and 'Kegel Exercises' exist. For detailed instructions on populating these, see `INSTRUCTIONS_Admin_WarmupCooldownKegel.txt`.

### Managing Equipment
*   Go to **Workouts > Equipment**.
*   Add, Edit, or Delete equipment types (e.g., 'Dumbbell', 'Barbell', 'Kettlebell', 'None' for bodyweight).
*   Includes a search field for equipment names.

### Managing Muscle Groups
*   Go to **Workouts > Muscle Groups**.
*   Add, Edit, or Delete muscle groups (e.g., 'Biceps', 'Pectoralis Major', 'Quadriceps').
*   **Interactive Muscle Map:** For a muscle group to appear on the 'Interactive Muscle Map' page, check the 'Show on map' box when adding/editing it.
*   Includes search and filter by 'Show on map'.

### Managing Exercises
*   Go to **Workouts > Exercises**.
*   Click 'ADD EXERCISE +' to add a new one, or click an existing exercise to edit.
*   Key fields to manage:
    *   **Name, Description, Instructions.**
    *   **Representative Image:** Upload an image for the exercise.
    *   **Video URL:** Link to an external demonstration video.
    *   **Difficulty, Is home friendly, Body focus.**
    *   **Workout category:** Assign to one or more categories.
    *   **Primary muscle group, Secondary muscle groups.**
    *   **Equipment:** Link required equipment.
    *   **Tags:** Assign relevant tags.
    *   **Contraindicated for diseases:** Crucial for user safety. Select any diseases for which this exercise is not recommended.
*   The exercise list is filterable and searchable.

### Managing Tags
*   Go to **Workouts > Tags**.
*   Add, Edit, or Delete tags (e.g., 'Cardio', 'Strength', 'PPL-Push'). The slug will auto-generate from the name.

## 5. Moderating User Contributions
*   Go to **Workouts > User Exercise Contributions**.
*   This lists all images/videos submitted by users for exercises.
*   **Review:** Check the uploaded image/video (links provided) and notes.
*   **Moderate:**
    *   Select one or more contributions using the checkboxes.
    *   From the 'Actions' dropdown, choose 'Mark selected contributions as Approved' or 'Mark selected contributions as Rejected'.
    *   Click 'Go'.
*   The user will see the updated status on their 'My Contributions' page. (Note: Approved contributions are not currently automatically displayed on exercise detail pages; this would be a further enhancement).

## 6. Nutrition Content Management

### Managing Nutrition Categories
*   Go to **Nutrition > Nutrition Categories**.
*   Add, Edit, or Delete categories like 'Breakfast', 'Lunch', 'Dinner', 'Snacks'.
*   Includes a search field.

### Managing Meal Recipes
*   Go to **Nutrition > Meal Recipes**.
*   Admins can Add, Edit, or Delete any recipe on the site, including those added by users.
*   Key fields: Name, User (creator), Description, Ingredients, Instructions, Times, Servings, Category, Image, Video URL.

## 7. Site Configuration & Maintenance

*   **Environment Variables:** Critical settings like `SECRET_KEY`, `DEBUG` mode, database connection details, and `MEDIA_ROOT` for shared files are managed via an `.env` file on the server, as outlined in `DEPLOYMENT_ON_PROXMOX_LXC.md`.
*   **Static Files:** Static files (CSS, JS, admin static files) are collected into a single directory during deployment (handled by the Dockerfile). If you make direct changes to static files on the server (not recommended, better to rebuild the Docker image), you might need to run:
    `docker compose exec web python manage.py collectstatic --noinput`
    (Assuming `manage.py` is at the root of your project in the container, adjust path if needed e.g. `python fitme_project/manage.py ...`)
*   **Database Backups:** Regularly back up your PostgreSQL database. This is a standard database administration task outside the direct scope of the Django application itself but crucial for production.

## 8. Troubleshooting (Admin Perspective)
*   **Server Logs:** If the site is down or behaving unexpectedly, check the Docker container logs:
    `docker compose logs web`
    `docker compose logs db`
*   **Django Admin History:** The admin panel for most objects shows a 'History' button, which can help track who changed what and when.
*   Refer to `DEPLOYMENT_ON_PROXMOX_LXC.md` for more technical troubleshooting related to the deployment environment.

---
This guide should help you effectively manage the FitMe website.
