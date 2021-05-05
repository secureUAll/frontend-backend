# Docker

To run, use docker compose.

> Use `--build` the first time or when you make changes that need a rebuild to take place. 

```bash
$ docker-compose up -d [--build]
```



The frontend app has hot code loading enabled (through a volume), so to apply changes made in Django there is no need to rebuild, only to stop and restart the containers (for nginx to restant the app).

```bash
$ docker-compose down && docker-compose up -d
```

