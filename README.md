# dj_zs

dj_zs - API template skeleton application based on Django for React/Vue frontend

## Features

- Custom-User-Model extend base model
- Authentication with JWT Tokens

## Screenshots

### [Click to see more](https://github.com/zergos1987/dj_zs/backend/app/media/screenshots)
![image](https://github.com/zergos1987/dj_zs/backend/app/media/screenshots/01.png)

## Installation

1. Clone the repository to use it localy:

        git clone https://github.com/zergos1987/dj_zs.git

2. In cloned/downloaded folder install backend requirements:

        pip install -r backend/requirements.txt
        
3. In project folder write command :
        `for Mac Users`
        ([ -d venv  ] && echo venv_activated || (python3 -m pip install virtualenv && python3 -m virtualenv venv && echo venv_created)) && source venv/bin/activate && pip install -r backend/requirements.txt && echo venv_activated && ([ -d app  ] && echo project dir exists || (source venv/bin/activate && django-admin startproject app && cd app && python3 manage.py startapp api && python3 manage.py startapp spa && cd .. && cp -R backend/app . && cp -R frontend/app . && ([ -f .env  ] && echo 1 || cp -R .env.example .env) && python3 app/manage.py makemigrations && python3 app/manage.py migrate && python3 app/manage.py collectstatic --no-input && echo ("from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@dj_zs.com', 'dj_zs12345')" | python3 app/manage.py shell) && echo init project dir done))
        
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
