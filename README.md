# dj_zs

dj_zs - api template skeleton application based on Django for React/Vue frontend

## Features

- Custom user Model extend base model
- Authentication with JWT Tokens

## Screenshots

### [Click to see more](https://github.com/zergos1987/dj_zs/backend/app/media/screenshots)
![image](https://github.com/zergos1987/dj_zs/backend/app/media/screenshots/01.png)

## Installation

1. First clone the repository to use it localy:

        git clone https://github.com/zergos1987/dj_zs.git

    Then install all required libraries  through:

        pip install -r backend/requirements.txt

2. Rename the `.env.example` to `.env`, then fill it with all the needed keys. `POSTGRES` is for the database access, `EMAIL` is for the email authentication and `SECRET_KEY` is the secret key for the application and etc.

3. Now you need to create a Postgre database with name `dj_zs` then do all the migrations using command:

        py manage.py makemigrations

    and:

        py manage.py migrate

4. For the frontend you need to run these commands from the `/frontend` folder:

        npm install

    to download all the needed NPM packages and then to start the frontend Dev server:

        npm run dev

5. Finally you can start the frontend server from base project folder by running:

        py manage.py runserver
