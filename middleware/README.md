# FastAPI + SQLModel + Alembic

docker-compose up -d --build
docker-compose down -v

## Alembic instructions

### initialization

```cmd
docker-compose exec web alembic init -t async migrations
docker-compose exec web alembic revision --autogenerate -m "init"
docker-compose exec web alembic upgrade head
```

### later making changes

make changes in models.py

apply update/create new migration file

```cmd
docker-compose exec web alembic revision --autogenerate -m "added project tables"
```

upgrade head

```cmd
docker-compose exec web alembic upgrade head
```
