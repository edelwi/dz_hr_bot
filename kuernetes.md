# Установка для версии 0 (telegram polling mode)

## Создание секретов

Секрет edelwicred на доступ в приватный репозиторий (DockerHub).

```shell
kubectl create secret docker-registry edelwicred --docker-server=https://index.docker.io/v1/ --docker-username=edelwi --docker-password=PASSWORD --docker-email=edelwi@yandex.ru
```

Секрет dz-hr-bot-token-cred с ткеном бота.

```shell
kubectl create secret generic dz-hr-bot-token-cred --from-literal=dz-hr-bot-token='BOT:TOKEN'
```

## Просмотр секретов

List:

```shell
kubectl get secrets
```

By name:

```shell
kubectl get secret dz-hr-bot-token-cred -o=yaml
```

With open secret:

```shell
kubectl get secret edelwicred --output="jsonpath={.data.\.dockerconfigjson}" | base64 --decode
```

## Установка

```shell
kubectl apply -f deploy_dz_hr_bot.yaml
```

deploy_dz_hr_bot.yaml:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: dz-hr-bot-app
spec:
  replicas: 1  # Количество реплик бота (polling supporte only 1)
  selector:
    matchLabels:
      app: dz-hr-bot
  template:
    metadata:
      labels:
        app: dz-hr-bot
    spec:
      containers:
      - name: dz-hr-bot
        image: edelwi/dz_hr_bot:0.0.1  # Имя и версия контейнера бота
        env:
          - name: BOT_TOKEN
            valueFrom:
              secretKeyRef:
                name: dz-hr-bot-token-cred
                key: dz-hr-bot-token
          - name: EDITORS
            value: "[1151496256, 453337448]"  # редактора, которые могут вызывать рассылку
          - name: CHATS
            value: "[-4067453977]"  # идентификаторы групп в которые бот будет слать сообщения
        resources:
          limits:
            memory: 400Mi
            cpu: 1
          requests:
            memory: 50Mi
            cpu: 100m
        ports:
        - containerPort: 8080
      imagePullSecrets:
      - name: edelwicred
```

## Удаление 

```shell
kubectl delete deployment dz-hr-bot-app
```
