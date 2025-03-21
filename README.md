# Mystic Tuner Backed

Business logic for the web application

Please see the documentation and development repository for system wide integration, architecture style and UML diagrams.

## Getting Started

1. Create a virtual environment

```bash
python -m venv venv
```

2. Activate the virtual environment

```bash
source venv/bin/activate
```

3. Change directory to the app folder

```bash
cd ./Mystic_Tuner_Backend
```

4.  Install the dependencies

```bash
pip install -r requirements.txt
```

5. Make a .env file in the Mystic_Tuner_Backend directory and add the following:

```bash
PORT = "" #Port to host frontend on
AUTH0_SECRET='' #secret associated with auth0 domain
APP_BASE_URL='' #where the app will be primarily hosted
AUTH0_DOMAIN='' #url to auth0 domain
AUTH0_CLIENT_ID='' 
AUTH0_CLIENT_SECRET=''
AUTH0_API_AUDIENCE = "" #url to auth0 apoi audience
AUTH0_ALGORITHMS = [""] #algorithm used to decode tokens
GEMINI_API_KEY = "" #key to authenticate user for gemini ai
DEBUG="" #wether or not the application is in debug mode
DJANGO_SECRET_KEY="" 
DJANGO_ALLOWED_HOSTS=""
CORS_ALLOWED_ORIGINS=""

DB_NAME="" #postgres database name
DB_USER="" #postgres username
DB_PASSWORD="" #postgres password
DB_HOST="" #where the server is located
DB_PORT="" #port that server is running on
```

6.  Run the development server (django)

```bash
python manage.py runserver
```

7. Open [http://localhost:5000](http://localhost:5000) with your browser to see the result.
8. Use Postman to test the API endpoints
