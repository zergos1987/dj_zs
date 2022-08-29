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

2. Install backend requirements from:

        pip install -r backend/requirements.txt
        
3. Rename the cloned/downloaded folder `dj_zs.git` with your `title` and inside this folder write:

        django-admin startproject app

4. Rename the `.env.example` to `.env`, then fill it with all the needed keys. 

5. Now you need to create a Postgre database and schema with name `dj_zs` and `app` then do all the migrations using command:

        py manage.py makemigrations

    and:

        py manage.py migrate

4. For the frontend you need to run these commands from the `/frontend` folder:

        npm install

    to download all the needed NPM packages and then to start the frontend Dev server:

        npm run dev

5. Finally you can start the frontend server from base project folder by running:

        py manage.py runserver
