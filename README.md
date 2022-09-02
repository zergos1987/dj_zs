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

2. In cloned/downloaded folder install backend requirements:

        pip install -r backend/requirements.txt
        
3. In project folder write command:

        django-admin startproject app

4. Rename the `.env.example` to `.env`, then fill it with all the needed keys. 

6. Copy and replace from folder `backend/app` && `fronted/app` to `project/app` folder.

7. Now you need to create a Postgres database and schema with name `dj_zs` and `app` then do all the migrations using command:

        python3 app/manage.py flush --no-input

    and:

        python3 app/manage.py makemigrations

    and:

        python3 app/manage.py migrate

    and:

        python3 app/manage.py collectstatic --no-input --clear

8. Finally you can start the frontend server from base project folder by running:

        python3 app/manage.py runserver
