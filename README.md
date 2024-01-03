# Longue vie aux objets, test


## INSTALLATION

### Install project
```
git clone <this git project>
```

### Create .env file and adapts it
```
cp .env.sample .env
vi .env
```

### Start services
```
docker compose up -d
```

### Migrate db
```
docker compose exec api python manage.py migrate
``` 

### Create super admin
```
docker compose exec api python manage.py createsuperuser
``` 