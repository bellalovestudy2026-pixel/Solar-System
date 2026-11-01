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
