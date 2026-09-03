# Todo List API

A beginner-friendly Todo List REST API built with Django, Django REST Framework, and MySQL.

## Features

- User registration
- Token-based login
- Authenticated task CRUD
- Users can only access their own tasks
- MySQL database support
- Django admin task management

## Tech stack

- Python 3
- Django
- Django REST Framework
- MySQL
- Postman or another API client

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

Install Django, Django REST Framework, and the MySQL driver in your environment. Keep the exact versions you install in a `requirements.txt` file before deploying.

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

Never commit your real `.env` file. The repository ignores `.env` files.

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

The tests cover password hashing, login tokens, authentication requirements, task ownership, and cross-user access protection.

## Security notes

- Secrets and database credentials are loaded from environment variables.
- Registration hashes passwords through Django's `create_user()`.
- Task ownership is assigned by the authenticated server-side user.
- Clients cannot change task ownership through the serializer.
- Protected endpoints require token authentication.

If a credential was ever committed to Git history, rotate that credential even after removing it from the current source.
