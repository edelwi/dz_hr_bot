# Dockerization

build container:

```shell
docker build -t dz_hr_bot .
```

login into docker registry (DockerHub)

```shell
docker login
```

push container into registry

```shell
docker push edelwi/dz_hr_bot:0.0.1   # check and correct tag name
```

run locale (check that bot with the same token is not running in kubernetes) :

```shell
docker run dz_hr_bot --env BOT_TOKEN='bot_token' --env EDITORS='[1151496256, 453337448]' --env='[-4067453977]'
```
