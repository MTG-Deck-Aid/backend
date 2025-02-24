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

1. Make a .env file in the Mystic_Tuner_Backend directory and add the following:

```bash
AUTH0_CLIENT_ID=''
AUTH0_CLIENT_SECRET=''
AUTH0_DOMAIN=''
```

7.  Run the development server (django)

```bash
python manage.py runserver
```

8. Open [http://localhost:8000](http://localhost:8000) with your browser to see the result.
9. Use Postman to test the API endpoints
