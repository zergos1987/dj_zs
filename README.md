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
        
2. In project folder write command:

For `Mac Users`

        ([ -d venv  ] && echo venv_activated || (python3 -m pip install virtualenv && python3 -m virtualenv venv && echo venv_created)) && source venv/bin/activate && pip install -r backend/requirements.txt && echo venv_activated && ([ -d app  ] && echo project dir exists || (source venv/bin/activate && django-admin startproject app && cd app && python3 manage.py startapp api && python3 manage.py startapp spa && cd .. && cp -R backend/app . && cp -R frontend/app . && ([ -f .env  ] && echo 1 || cp -R .env.example .env) && python3 app/manage.py makemigrations && python3 app/manage.py migrate && python3 app/manage.py collectstatic --no-input && echo ("from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@dj_zs.com', 'dj_zs12345')" | python3 app/manage.py shell) && echo init project dir done))

For `Windwos Users`
        
3. Run backend command:

        python3 app/manage.py runserver
