# e-secretary
E-Secretary is a proposed solution for a university's secretary website, developed as a semester project in the Web Programming Course at ECE Dept. University of Patras

## Installation

Clone this git repo and setup python virtual environment (Python 3.7 recommended).

```bash
git clone https://github.com/tsikup/e-secretary
cd e-secretary
python -m venv web_project
```

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all dependencies.

```bash
pip install -r requirements.txt
```

## Database

### Docker

Install `docker` for your linux distro or run `curl https://get.docker.com | sh` to install it manually

Setup a docker container for mariadb on port `50000` with db_user `admin` with pass `qwe123` and db `e_university`. Remember to replace the `root_pass`.

```bash
docker run --name mariadb \
-e MYSQL_ROOT_PASSWORD=root_pass \
-e MYSQL_USER=admin \
-e MYSQL_PASSWORD=qwe123 \
-e MYSQL_DATABASE=e_university \
-d mariadb:latest
```

The previously created DB is empty. If you have been provided with the DB data use the next command to create the db and also mount the designated volume. Remember to replace the `root_pass` and `/path/to/mariadb/data`.

```bash
docker run --name mariadb \
-e MYSQL_ROOT_PASSWORD=root_pass \
-e MYSQL_USER=admin \
-e MYSQL_PASSWORD=qwe123 \
-e MYSQL_DATABASE=e_university \
-v /path/to/mariadb/data:/var/lib/mysql \
-d mariadb:latest
```

### Build Database

If the DB is empty run the following commands, else skip this. This also creates the admin user (superuser).

```bash
manage.py makemigrations
manage.py migrate
manage.py createsuperuser
```

## Run Server

```bash
manage.py runserver
```

The web app will run in development. In order to go to production please refer to the django docs or the [Mozilla Django Docs](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Deployment).

## Access admin panel

In order to access the admin panel, which is also used as the secretary web panel, go to 

`http://localhost:port/admin`

Port number for development is `8000`

Create user groups for `Professors` and `Students` and assign each one with the respective permissions. Then create users (Professors and Students) and add them to their corresponding group.