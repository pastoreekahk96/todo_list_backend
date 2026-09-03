# Todo List API

A beginner-friendly Todo List REST API built with Django, Django REST Framework, and MySQL.

## Features

- User registration with Django password validation
- Token-based authentication
- Token logout/invalidation
- Authenticated task CRUD
- Users can only access their own tasks
- API request throttling for anonymous and authenticated clients
- MySQL database support
- Django admin task management
- Automated tests and GitHub Actions CI

## Tech stack

- Python 3.10+
- Django 5.2 LTS
- Django REST Framework
- MySQL
- Postman or another API client
- GitHub Actions

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/pastoreekahk96/todo_list_backend.git
cd todo_list_backend
```

### 2. Create and activate a virtual environment

Linux/macOS:

```bash
python3 -m venv env
source env/bin/activate
```

Windows PowerShell:

```powershell
python -m venv env
.\env\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure environment variables

Do not put secrets directly in `config/settings.py`.

Set these variables in your local environment:

```text
DJANGO_SECRET_KEY=replace-with-a-long-random-secret
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
DJANGO_SECURE_SSL_REDIRECT=False
MYSQL_DATABASE=todo_db
MYSQL_USER=todo_user
MYSQL_PASSWORD=your-database-password
MYSQL_HOST=localhost
MYSQL_PORT=3306
```

For production, use a real secret manager or protected environment variables. Do not commit your real `.env` file.

### 5. Apply migrations

```bash
python manage.py migrate
```

### 6. Run the development server

```bash
python manage.py runserver
```

The API is available under `/api/`.

## API endpoints

| Method | Endpoint | Authentication | Purpose |
|---|---|---|---|
| POST | `/api/register/` | No | Create an account |
| POST | `/api/login/` | No | Get an authentication token |
| POST | `/api/logout/` | Token | Invalidate the current user's token |
| GET | `/api/tasks/` | Token | List your tasks |
| POST | `/api/tasks/` | Token | Create a task |
| GET | `/api/tasks/<id>/` | Token | Get one of your tasks |
| PUT | `/api/tasks/<id>/` | Token | Update one of your tasks |
| DELETE | `/api/tasks/<id>/` | Token | Delete one of your tasks |

For protected endpoints, send:

```text
Authorization: Token YOUR_TOKEN
```

## Testing

Run the Django test suite with:

```bash
python manage.py test
```

The tests cover:

- Password hashing
- Weak-password rejection
- Login behavior
- Missing credentials
- Token logout/invalidation
- Authentication requirements
- Task ownership
- Cross-user read, update, and delete protection
- Protection against client-controlled task ownership

GitHub Actions runs Django checks, database migrations, and the test suite against MySQL.

## Security notes

- Secrets and database credentials are loaded from environment variables.
- Production mode enables secure session and CSRF cookies, content-type sniffing protection, frame protection, and strict referrer policy.
- Registration uses Django's password hashing and password validators.
- Protected API endpoints require token authentication.
- Anonymous and authenticated API requests are throttled to reduce abuse.
- Task ownership is assigned by the authenticated server-side user.
- Clients cannot change task ownership through the serializer.
- Logout deletes the user's token.

### Credential rotation

If a credential was ever committed to Git history, rotate that credential even after removing it from the current source. Removing a secret from the latest commit does not make an exposed credential safe.

## Development checklist

Before deploying changes:

```bash
python manage.py check
python manage.py test
```

For production, run Django's deployment checks with the appropriate production environment variables and HTTPS configuration:

```bash
python manage.py check --deploy
```
