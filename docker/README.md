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



## Auxiliar script

For development purposes, Django folder is mapped as a volume inside the container, so that changes made to the code do not require the rebuild of the project. However, this can generate conflicts with the migrations files when the database folder is removed. To help solving this conflicts, before every build (only when using `--build` argument), run the script `dockerclean.sh`.

```bash
$ sudo ./dockerclean.sh
$ docker-compose up -d --build
```

