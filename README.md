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

Run server

```shell script
python manage.py runserver
```
