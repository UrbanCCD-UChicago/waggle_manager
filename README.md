# Waggle Manager

Device Management Studio for Beehive v2

Right now, this is a proof of concept: it has the database design codified in a Django
app so that we have a simple way to write up tests to prove the design.

It's also a decent enough platform to design applications on top of, so assuming this
works out we can just roll with it.

## Development

### Pipenv for dependency management

Why? Because packaging and dependency management is broken beyond belief
in the Python world, and this injects so sanity and standards.

Here's a super quick run through:

- `pipenv install` to install the runtime deps in the Pipfile
- `pipenv install --dev` to install the development deps in the Pipfile
- `pipenv install <package name>` to install a runtime app dependency
- `pipenv install --dev <package name>` to install a dev dependency
- `pipenv shell` to wrap your shell in the python virtualenv
- `pipenv run <command>` to wrap your command with the virtualenv

### Running the database

This requires PostGIS to run. The easiest way to get that up and running (and 
configured for the app) is using Docker:

```bash
$ docker pull mdillon/postgis
$ docker run -p 5432:5432 -e POSTGRES_PASSWORD=password -e POSTGRES_DB=waggle_manager mdillon/postgis
```

You'll then need to run the migrations:

```bash
$ pipenv run python manage.py migrate
```

### Runing the development server

Once you've stood up your database, you can run the dev server with:

```bash
$ pipenv run python manage.py runserver
```

If you haven't created a superuser yet, you can do that with:

```bash
$ pipenv run python manage.py createsuperuser
```

As of now, all we have is the built in admin site: http://localhost:8000/admin .

### Running the tests

You guessed it:

```bash
$ pipenv run python manage.py test
```
