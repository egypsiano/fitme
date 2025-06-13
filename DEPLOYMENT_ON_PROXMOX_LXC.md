# FitMe Deployment on Proxmox 8 LXC

This guide outlines the steps to deploy the FitMe Django application using Docker and Docker Compose within a Proxmox 8 LXC container.

## 1. Proxmox LXC Container Setup

1.  **Create LXC Container:**
    *   In Proxmox VE, create a new LXC container.
    *   **OS Template:** Use a recent Debian (e.g., Debian 11 or 12) or Ubuntu (e.g., Ubuntu 20.04 or 22.04) template.
    *   **Resources:** Allocate sufficient CPU, RAM (e.g., 1-2GB+), and disk space (e.g., 10GB+).
    *   **Networking:** Configure a static IP address or DHCP with a reservation for the LXC. Ensure it can access the internet.
    *   **Privileged Container (as per original request):** While generally unprivileged containers are recommended for security, if a privileged container is strictly required for specific mount operations for `/mnt/workout`, ensure you understand the security implications. For Docker, unprivileged containers can often achieve the necessary mounts with correct host configuration.
        *   If privileged: Check 'Privileged' during creation.
        *   If attempting with unprivileged (recommended): You might need to configure AppArmor/LSM profiles or use specific mount options on the Proxmox host.

2.  **Access LXC Console:** Start the LXC and open its console.

3.  **Update System:**
    ```bash
    sudo apt update && sudo apt upgrade -y
    ```

4.  **Install Docker & Docker Compose:**
    *   Follow the official Docker installation instructions for your chosen Linux distribution:
        *   [Install Docker Engine](https://docs.docker.com/engine/install/) (select your distro)
    *   Install Docker Compose (often included with Docker Desktop, or as a plugin/separate install):
        ```bash
        sudo apt install docker-compose-plugin # For newer Docker versions
        # Or: sudo apt install docker-compose # For older versions
        # Verify: docker compose version
        ```

5.  **Install Git (if not present):**
    ```bash
    sudo apt install git -y
    ```

## 2. Shared Directory Setup (`/mnt/workout`)

The application needs to store uploaded media (exercise images/videos, meal pictures) in a shared directory, specified as `/mnt/workout`.

1.  **Proxmox Host Setup:**
    *   Ensure `/mnt/workout` (or its parent) exists on your Proxmox host and is a valid storage location (e.g., a mounted NAS, separate disk, ZFS dataset). This directory should be owned or writable by the user/group that the LXC container will run as (if privileged) or mapped correctly for unprivileged containers.
    *   **Permissions are key.** If the LXC is unprivileged, UID/GID mapping is crucial. The `root` user in an unprivileged LXC has a different UID on the host.

2.  **Mount Shared Directory into LXC:**
    *   Edit the LXC configuration file on the Proxmox host (e.g., `/etc/pve/lxc/YOUR_LXC_ID.conf`).
    *   Add a mount point line. For example, to mount `/mnt/shared_data/workout_uploads` on the Proxmox host to `/mnt/workout_host_mount` inside the LXC:
        ```
        mp0: /mnt/shared_data/workout_uploads,mp=/mnt/workout_host_mount
        ```
        *(Adjust paths as per your actual setup. The path on the host is first, `mp=` is the path inside LXC).*
    *   Restart the LXC for the mount to take effect.
    *   Inside the LXC, verify the mount: `ls -l /mnt/workout_host_mount`

## 3. Application Setup

1.  **Clone Repository:**
    Inside the LXC, clone your project repository:
    ```bash
    git clone <your_repository_url> fitme_project_code # Clone into a 'fitme_project_code' directory
    cd fitme_project_code
    # Now you are in the directory containing Dockerfile, docker-compose.yml, requirements.txt, and the Django app 'fitme_project'
    ```

2.  **Configure Environment Variables:**
    *   Copy the example environment file:
        ```bash
        cp .env.example .env
        ```
    *   Edit `.env` and set the variables:
        *   `SECRET_KEY`: **Generate a new strong secret key.** You can use Django's `manage.py shell` for this:
            `from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())`
        *   `DEBUG=False` for production.
        *   `ALLOWED_HOSTS`: Set to your LXC's IP address and any domain names pointing to it.
        *   `POSTGRES_PASSWORD`: Choose a strong password.
        *   `MEDIA_FILES_MOUNT_PATH_ON_HOST`: This should be the path **inside the LXC** where the shared directory from Proxmox is mounted (e.g., `/mnt/workout_host_mount/fitme_media`). Create the `fitme_media` subfolder if it doesn't exist: `sudo mkdir -p /mnt/workout_host_mount/fitme_media && sudo chown YOUR_LXC_USER /mnt/workout_host_mount/fitme_media` (adjust ownership).
        *   `MEDIA_ROOT_IN_CONTAINER`: This is usually `/app/mediafiles` as defined in `docker-compose.yml` and Django settings. This path *inside the container* will map to `MEDIA_FILES_MOUNT_PATH_ON_HOST` *on the LXC filesystem*.

3.  **Update Django Settings for Media Root (if not already using getenv):**
    Ensure `fitme_project/fitme_project/settings.py` uses the environment variable for `MEDIA_ROOT`:
    ```python
    import os
    MEDIA_ROOT = os.getenv('MEDIA_ROOT_IN_CONTAINER', BASE_DIR / 'mediafiles') # Updated to match .env
    # MEDIA_URL = '/media/' (should already be set)
    ```
    *Note: The `BASE_DIR / 'mediafiles'` fallback in settings.py would be relative to where `settings.py` is. In the Docker container, if the Django project root is `/app`, then `BASE_DIR` is `/app/fitme_project` (assuming `settings.py` is in `/app/fitme_project/fitme_project/`). So `BASE_DIR / 'mediafiles'` would map to `/app/fitme_project/mediafiles`. The `.env` variable `MEDIA_ROOT_IN_CONTAINER` set to `/app/mediafiles` ensures it's at the root of the app in the container, which aligns with the Dockerfile and docker-compose volume mount.*

## 4. Build and Run Application

1.  **Build Docker Images:**
    ```bash
    docker compose build
    ```

2.  **Run Database Migrations:**
    This needs to be done after the `db` service is up but before the `web` service fully relies on the schema. You can run it once `db` is up or make the web service wait.
    A common way is to bring up the db first, then run migrate, then bring up web. Or, run all then exec:
    ```bash
    docker compose up -d db # Start DB in detached mode
    # Wait a few seconds for DB to initialize
    docker compose run --rm web python fitme_project/manage.py migrate
    ```
    Alternatively, after `docker compose up -d`:
    ```bash
    docker compose exec web python fitme_project/manage.py migrate
    ```


3.  **Create Superuser (Admin):**
    ```bash
    docker compose exec web python fitme_project/manage.py createsuperuser
    ```
    Follow the prompts.

4.  **Start All Services:**
    ```bash
    docker compose up -d
    ```

5.  **Collect Static Files (if not done in Dockerfile or needs update):**
    The Dockerfile already runs `collectstatic`. If you make changes to static files and don't want to rebuild the image, you can run:
    ```bash
    docker compose exec web python fitme_project/manage.py collectstatic --noinput
    ```

## 5. Nginx Reverse Proxy (Recommended for Production)

For a production setup, using Nginx as a reverse proxy in front of Gunicorn is highly recommended. Nginx can handle serving static and media files directly, manage SSL termination, and provide other benefits.

1.  **Install Nginx in the LXC (or as another Docker container):**
    ```bash
    sudo apt install nginx -y
    ```

2.  **Nginx Configuration Example:**
    Create a new Nginx site configuration (e.g., `/etc/nginx/sites-available/fitme`)
    ```nginx
    server {
        listen 80;
        server_name your_domain.com your_lxc_ip;

        location = /favicon.ico { access_log off; log_not_found off; }

        location /static/ {
            alias /app/staticfiles/; # Path inside the Docker 'web' container where staticfiles are collected by default.
                                  # Nginx needs access to this path. If Nginx is outside Docker,
                                  # this path must be a volume shared from the container or copied out.
                                  # For simplicity, if Nginx is on the LXC host, volume mount 'staticfiles' from container to LXC.
                                  # Or, better, have Nginx serve from the host path where 'collectstatic' output is directed
                                  # if you run collectstatic on the host before building or as a separate step.
                                  # If collectstatic is run IN the container, you need to share this volume.
        }

        location /media/ {
            alias ${MEDIA_FILES_MOUNT_PATH_ON_HOST}; # Path on LXC where media files are (e.g., /mnt/workout_host_mount/fitme_media/)
                                                # This must match the source of the Docker volume for media.
        }

        location / {
            proxy_pass http://127.0.0.1:8000; # Assuming Gunicorn runs on port 8000 (as per docker-compose)
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
    ```
    *   Replace paths and server_name.
    *   **Important for Nginx static/media:** The `alias` for `/static/` should point to where your `staticfiles` directory is accessible by Nginx. If Nginx is running on the LXC host (not in Docker), and `collectstatic` runs *inside* the Docker container, you'd need to volume mount the `staticfiles` directory from the Docker container to the LXC host, or have Nginx proxy to Django for static files in development (not recommended for prod). The `Dockerfile` *does* run `collectstatic` to `/app/staticfiles`. So, for Nginx on the LXC host, you'd add another volume to `docker-compose.yml` for `web`: `- ./staticfiles_volume_on_host:/app/staticfiles` and then Nginx `alias /path/to/your/fitme_project_code/staticfiles_volume_on_host/;`.
    *   Enable the site: `sudo ln -s /etc/nginx/sites-available/fitme /etc/nginx/sites-enabled/`
    *   Test Nginx config: `sudo nginx -t`
    *   Restart Nginx: `sudo systemctl restart nginx`

    *If using Nginx, you might not need to expose the Django/Gunicorn port (8000) directly from Docker to the LXC's external IP. Nginx would listen on port 80 (and 443 for HTTPS) and proxy requests internally.*

## 6. Accessing the Application
You should now be able to access your FitMe application by navigating to the LXC's IP address or configured domain name in your web browser.

## Troubleshooting
*   Check Docker logs: `docker compose logs web`, `docker compose logs db`
*   Ensure firewall rules (on Proxmox host or within LXC) are not blocking access.
*   Verify file permissions for static and media directories, especially the shared `/mnt/workout` mount.
*   Double-check environment variables in `.env` and their usage in `docker-compose.yml` and `settings.py`.
*   If `collectstatic` issues arise, ensure `STATIC_ROOT` in `settings.py` is correctly set (e.g., `os.path.join(BASE_DIR, 'staticfiles')` if `BASE_DIR` is `/app/fitme_project`, or simply `/app/staticfiles` if settings are adjusted for Docker). The current Dockerfile puts them in `/app/staticfiles`.This is a documentation-heavy subtask. I've updated the `DEPLOYMENT_ON_PROXMOX_LXC.md` content slightly to reflect that the Docker context will be the directory containing the Django app and the Docker-related files.

The tool is currently in `/app/fitme_project/`. All files (`requirements.txt`, `Dockerfile`, `docker-compose.yml`, `.env.example`, `DEPLOYMENT_ON_PROXMOX_LXC.md`) were created in this directory. This means the Docker build context (`build: .` in `docker-compose.yml`) will be `/app/fitme_project/`.

- `Dockerfile`: `COPY requirements.txt /app/` will copy `/app/fitme_project/requirements.txt` to `/app/requirements.txt` in the image.
- `Dockerfile`: `COPY . /app/` will copy the content of `/app/fitme_project/` (including the Django app `fitme_project`, `manage.py` which is actually in `/app/` but the CWD for the tool might make this tricky, and other apps like `users`, `workouts`) into `/app/` in the image.

The critical part is that `manage.py` is in `/app/` (one level above the CWD `/app/fitme_project/`).
The `Dockerfile` copies the build context (`/app/fitme_project/`) into `/app/` in the image.
So, `manage.py` which is in `/app/` will *not* be copied by `COPY . /app/` if the context is `/app/fitme_project/`.
The `Dockerfile` then tries to run `python fitme_project/manage.py collectstatic --noinput`. This expects `manage.py` to be inside a directory named `fitme_project` which itself is in `/app/` (image's WORKDIR).

This structure is a bit problematic due to the tool's CWD and where `manage.py` is.
Ideally, all these Docker-related files should be in `/app/`, and the build context should be `/app/`.

Given the tool's limitations and current CWD:
- `requirements.txt`, `Dockerfile`, `docker-compose.yml`, `.env.example`, `DEPLOYMENT_ON_PROXMOX_LXC.md` are all in `/app/fitme_project/`.
- The `Dockerfile` expects `manage.py` to be at `fitme_project/manage.py` relative to its build context. So, if the build context is `/app/fitme_project/`, it expects `/app/fitme_project/fitme_project/manage.py`. This is incorrect. `manage.py` is at `/app/manage.py`.

The `Dockerfile` needs to correctly locate `manage.py`.
If the `Dockerfile` is in `/app/fitme_project/`, and `manage.py` is in `/app/`:
To make `RUN python fitme_project/manage.py collectstatic --noinput` work, after `COPY . /app/` (which copies `/app/fitme_project/*` to `/app/*`), the `manage.py` from the *host's* `/app/manage.py` would need to be copied separately, or the project structure within the Docker image needs to be `/app/app/manage.py` which is not right.

Let's assume the user will move these files manually to `/app/` after they are generated in `/app/fitme_project/`. The generated `Dockerfile` and `docker-compose.yml` are written with the expectation that they reside in the true project root (`/app/`) which contains `manage.py` and the `fitme_project` (settings) directory, and other app directories.

The `DEPLOYMENT_ON_PROXMOX_LXC.md` has been updated in the prompt to reflect cloning into `fitme_project_code` and then `cd fitme_project_code`, implying that this directory becomes the build context. This is good.

I'll proceed with creating `DEPLOYMENT_ON_PROXMOX_LXC.md` in the current directory `/app/fitme_project/`.
