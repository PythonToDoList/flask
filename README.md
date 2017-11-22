# To Do List - Flask Implementation

**Author**: Nicholas Hunt-Walker

**Deployment**: https://flask-tasklist.herokuapp.com/

**Python Versions**: 3.6+ only

## Getting Started

Navigate to a directory that you want to work in and clone down this repository.

```
$ git clone https://github.com/PythonToDoList/flask.git
```

### For Development

Move into the cloned directory and start a new Python 3 [virtual environment](https://docs.python.org/3/tutorial/venv.html). You should be using Python 3.6 or later.

```
$ cd pyramid
pyramid $ python3 -m venv ENV
(ENV) flask $ source ENV/bin/activate
```

[pip](https://pip.pypa.io/en/stable/installing/) install this repository's `requirements.txt`.
Note: you will need [Postgres](https://www.postgresql.org) running locally for this application.

```
(ENV) flask $ pip install -r requirements.txt
```

In your virtual environment, set as environment variables the URL to the Postgres database that you intend to use for development, as well as the `FLASK_APP` environment variable with the path to the repository's `app.py` file.
For something closer to bulletproof, use the absolute path to the file.
Note that on my machine I don't need a username or password to access my postgres databases, but your own results may vary.

```
export DATABASE_URL=postgres://localhost:5432/flask_todo
export FLASK_APP=$VIRTUAL_ENV/../flask_todo/app.py
```

Initialize your database using the provided `initializedb.py` file.
If you want to be able to drop tables before you create them, set an environment variable of `DEVELOPMENT` to `'True'`.

```
(ENV) flask $ python initializedb.py
```

In order to run the application, type `flask run`.
If all your stuff is configured properly, your development server should be running on port 5000.

### For Deployment (Heroku)


Sources:
    - http://blog.luisrei.com/articles/flaskrest.html
    - http://flask-httpauth.readthedocs.io/en/latest/
    - https://stackoverflow.com/questions/13825278/python-request-with-authentication-access-token
    - http://flask.pocoo.org/snippets/30/
