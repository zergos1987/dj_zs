# dj_zs

dj_zs - api template skeleton application based on Django for React/Vue frontend

## Features

- Custom user Model extend base model
- Authentication with JWT Tokens

## Screenshots

### [Click to see more](https://github.com/zergos1987/dj_zs/backend/app/media/screenshots)
![image](https://github.com/zergos1987/dj_zs/backend/app/media/screenshots/01.png)

## Installation

1. Clone the repository to use it localy:

        git clone https://github.com/zergos1987/dj_zs.git

2. Rename the cloned/downloaded folder `dj_zs.git` with your project folder `title` and in project folder install backend requirements:

        python3 -m venv venv && source venv/bin/activate && pip install -r backend/requirements.txt
        
3. In project folder write command:

        django-admin startproject app

4. Rename the `.env.example` to `.env`, then fill it with all the needed keys. 


5. Now you need to create a Postgres database and schema with name `dj_zs` and `app` then do all the migrations using command:

        python3 manage.py flush --no-input

    and:        
        python3 manage.py makemigrations

    and:

        python3 manage.py migrate

6. For the frontend you need to run these commands from the `/frontend` folder:

        npm install

    to download all the needed NPM packages and then to start the frontend Dev server:

        npm run dev

7. Finally you can start the frontend server from base project folder by running:

        py manage.py runserver
