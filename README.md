# DJANGO


## Dependence

* [Python](https://www.python.org/) 3.8
* [Django](https://www.djangoproject.com/) 3.1.5

## Get Started

```
$ docker-compose up --build

$ docker-compose down --rmi all --volumes --remove-orphans
```

```
$ docker container exec -it python sh
```

### Development

- Main site
    - http://localhost:8888

- Admin page
    - http://localhost:8888/admin

- Scheduler page
    - http://localhost:8888/scheduler

### Commands
create a django app
```
$ docker exec python ./manage.py startapp {app_label}
```

create models from existing database
```
$ docker exec python ./manage.py inspectdb > {path/to/models.py}
```

execute migration
```
$ docker exec python ./manage.py migrate
```

create a migration file
```
$ docker exec python ./manage.py makemigrations
```

create dump fixture files
```
$ docker exec python ./manage.py dumpdata {app_label.model} --indent 2 > {path/to/fuxture.json}
```

load data from fixture files
```
$ docker exec python ./manage.py loaddata --verbosity 2 > {path/to/fuxture.json}
```

create an admin account
```
$ docker exec -it python ./manage.py createsuperuser
```

## ECサイトを利用した管理画面の作成

### 参考
https://h-memo.com/django-oscar-ec/

python manage.py migrate
python manage.py collectstatic
python manage.py oscar_populate_countries
