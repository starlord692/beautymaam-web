# Beauty Maam Grooming Studio

Luxury beauty parlour web application built with Django.

## Features
- **Public Website**: Home, About, Services, Gallery, Contact.
- **Online Booking**: Schedule appointments for Parlour or Home services.
- **Services**: Grouped by category, with dynamic pricing.
- **Admin Dashboard**: Manage staff, appointments, and services.
- **Responsive Design**: Mobile-first luxury UI.

## Local Development Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Variables**:
   Create a `.env` file in the root directory:
   ```env
   DEBUG=True
   SECRET_KEY=your-secret-key-temp
   # DATABASE_URL=sqlite:///db.sqlite3 (Default if not set)
   CLOUDINARY_CLOUD_NAME=your_cloud_name
   CLOUDINARY_API_KEY=your_api_key
   CLOUDINARY_API_SECRET=your_api_secret
   ```

3. **Migrate Database**:
   ```bash
   python manage.py migrate
   ```

4. **Create Superuser**:
   ```bash
   python manage.py createsuperuser
   ```

5. **Run Server**:
   ```bash
   python manage.py runserver
   ```

## Production Deployment (Render)

This project is configured for deployment on Render.com with Gunicorn, WhiteNoise, and PostgreSQL.

### 1. Prerequisites
- A GitHub repository with this code.
- A Cloudinary account for media hosting.

### 2. Deployment Steps
1. **Create a New Web Service** on Render connected to your GitHub repo.
2. **Environment**: Select `Python 3`.
3. **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   *(Note: Render often runs collectstatic automatically, but adding it here is safe)*
4. **Start Command**: `gunicorn config.wsgi --log-file -`

### 3. Environment Variables
Add the following variables in the Render Dashboard:

| Variable | Value |
|----------|-------|
| `PYTHON_VERSION` | `3.10.0` (or greater) |
| `SECRET_KEY` | Generate a strong random string |
| `DEBUG` | `False` |
| `DATABASE_URL` | (Render provides this if you attach a Postgres DB) |
| `CLOUDINARY_CLOUD_NAME` | Your Cloud Name |
| `CLOUDINARY_API_KEY` | Your API Key |
| `CLOUDINARY_API_SECRET` | Your API Secret |
| `ALLOWED_HOSTS` | `*` (or your specific domain) |

### 4. Database
- Create a **New PostgreSQL** database on Render.
- Link it to your Web Service. Render will automatically inject `DATABASE_URL`.
- The `Procfile` includes a release command that will run `python manage.py migrate` automatically on every deploy.

## Admin Features
Access the admin panel at `/admin/dashboard/` or standard Django admin at `/admin/`.
- Manage Services and Categories.
- View and Approve Appointments.
- Manage Staff and Gallery.
