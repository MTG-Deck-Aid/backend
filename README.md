# Mystical Tuner Backend

Business logic for the web application

## Local Development

Using a virtual enviroment is required for this project. Only the required dependencies should be installed on the production server.
Please follow the steps below to understand why this is important and how to set up a virtual environment.

### Dependencies

It is critical to have all the requirments in the `requirements.txt` file installed. This can be done by running the following command:

```bash
pip freeze > requirements.txt
```

If you did this with a global python environment, you will have old project dependencies in the `requirements.txt` file. This is why it is important to use a virtual environment.

### Using a virtual environment

1. Create a virtual environment

```bash
python -m venv venv
```

2. Activate the virtual environment

```bash
source venv/scripts/activate
```

3. Confirm that the virtual environment is activated. Top file is the python interpreter in use.

```bash
where python
```

### Install dependencies

With the venv activated, install the dependencies

```bash
pip install -r requirements.txt
```
