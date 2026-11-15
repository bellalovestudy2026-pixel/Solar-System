# Study Hub

A local Django learning project. The original `solar_system.html` is preserved separately.

## Run on Windows PowerShell

From this repository folder, run:

```powershell
.\.venv\Scripts\python.exe manage.py runserver
```

Open http://127.0.0.1:8000/ for Study Hub or http://127.0.0.1:8000/science/ for Science Study. Keep the terminal running; press Ctrl+C to stop the server. This command works without activating the virtual environment.

To activate optionally:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned -Force
.\.venv\Scripts\Activate.ps1
```

After activation, `python manage.py runserver` also works.

## Student accounts

- `/accounts/signup/` uses Django's `UserCreationForm` to validate usernames and passwords and store hashed passwords. Successful registration redirects to login.
- `/accounts/login/` uses Django's `LoginView` and its built-in authentication form to start a session. Successful login redirects home (or to a safe local `next` URL).
- `/accounts/logout/` uses Django's `LogoutView`. The navigation submits a CSRF-protected POST form to end the session and return home.
- `learning/views.py` adds the sign-up view; `learning/urls.py` names the three account routes. `config/settings.py` sets the login and logout destinations.
- `learning/templates/learning/login.html` and `signup.html` render forms, validation errors, and CSRF tokens. `base.html` shows account links or a logout button; `home.html` displays the signed-in student's username using Django's existing auth context processor.

Apply built-in database migrations before first use, then run the local checks:

```powershell
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py test
```

Tests cover guest pages, registration and validation, password hashing, login errors, username display, safe redirects, POST-only logout, session clearing, and CSRF protection. Tests use a separate temporary database.

To try it in a browser, run the server, sign up, log in, check the welcome message on the home page, and click **Log out**. The welcome message disappears and the login/sign-up links return.

## How the pages connect

- `config/settings.py`: project settings, including the registered `learning` app.
- `config/urls.py`: sends page requests to `learning/urls.py`.
- `learning/urls.py`: maps addresses to views and gives each route a name.
- `learning/views.py`: Python functions that select templates to render (turn into HTML).
- `learning/templates/learning/base.html`: shared page layout and styles.
- `learning/templates/learning/home.html`: home page.
- `learning/templates/learning/science.html`: Science Study page.

To add Math or English, add a view, a named URL, and a template following Science's pattern. Replace the corresponding home page placeholder with a link using Django's `url` template tag.

The Science Study page links to the solar system explorer at http://127.0.0.1:8000/science/solar-system/. Django renders the app template `learning/templates/learning/solar_system.html`. Edit that template to update the explorer in Django. The original root `solar_system.html` is preserved separately. Use your browser's Back button to return to Science Study.
