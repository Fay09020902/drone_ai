## Local Development

### First-time setup

1. Backend

```shell
<root> % pipenv install
```

2. Frontend

```shell
<root> % npm install
```
3. Activate the backend virtual environment

```shell
<root> % pipenv shell
```
4. Run the flask server

```shell
<root> % pipenv run flask run
```

5. Start the frontend React application

```shell
<frontend> % npm start
```

 If any environment variables are required (such as API keys), make sure they are configured locally in .flaskenv files.
