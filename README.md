


# DB MIGRATIONS #
### Creating magrations:

Inside a container (api or daemon) run:

To generate only migration use `./scripts/create_alembic_revision`

Or inside smtv-api container run:

```bash
# 1. To generate new migration
alembic revision --autogenerate -m "add id FK to user model"
# 2. To update DB
alembic upgrade head
```


## Poligon (not well desribe but useful commands - TODO later)

Offiline migration run:
```
docker exec -it smtv-micro-scpr_api_1 alembic revision --autogenerate -m "init_db"
``` 

