# mozio_service

## Setup

### Step 1

Create database and a user in postgres.

```sql
CREATE DATABASE mozio;
```

```sql
CREATE USER mozio WITH PASSWORD 'Mozio@123';
```

```sql
GRANT ALL PRIVILEGES ON DATABASE mozio TO mozio;
```

```sql
ALTER USER mozio WITH SUPERUSER;
```

### Step 2
Install postgis
```
sudo apt install postgis
```

Create postgis extension.

```sql
CREATE EXTENSION postgis;
```

### Step 3

Installing Geospatial libraries

```
https://docs.djangoproject.com/en/4.0/ref/contrib/gis/install/geolibs/
```

### Step 4

Run tests

```shell script
python manage.py test
```

### Step 5

Run server

```shell script
python manage.py runserver
```
