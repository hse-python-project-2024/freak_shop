# Жуткая лавка

Адаптация настольной карточной игры о торговле страхом.

Правила игры вы можете найти на этом [сайте](https://www.mosigra.ru/download/%D0%9F%D1%80%D0%B0%D0%B2%D0%B8%D0%BB%D0%B0/Zhutkaua_lavka_rules.pdf)
# Сервер:

## Игра в локальной сети:

Предположим что вы склонировали этот git репозиторий, находитесь в корневой директории и хотите поднять свой сервер.

Если вы хотите запустить всё в своей локальной сети, то для этого вам нужно создать базу данных и заполнить конфиги
следующим образом:

server/config.py:

```
db_host = "127.0.0.1"  # или хост вашей базы данных
db_port = "5432"  # другое значение, если PostgreSQL слушает нестандарнтый порт
db_user_name = "freak_shop_owner"  # имя пользователя, имеющего доступ к бд
db_password = "password"  # пароль пользователя, которого мы указали
db_name = "freak_shop"  # название базы данных

host = "localhost"
port = "50051" 
```

При первом запуске выполните:
```
make drop_and_restore_data_base
make prepare_server
```
Первая команда сбросит схему freak_shop (если она существовала), создаст новую с нужными табличками и далее сервер будет обращаться к этой схеме. Вторая подготовит ваш сервер к выполнению (создать python окружение для работы, скачает туда все зависимости и раскроет необходимые proto файлы)

Теперь, если вы хотите запустить ваш сервер, просто выполните:
```
make run_server
```

Поздравляю! Ваш сервер поднят и готов принимать соединения

Если после завершения ваших личных игровых сессий вы поймете, что хотите удалить все созданные файлы для работы, просто выполните 
```
make clean_server
```
Если сервер вам вообще больше никогда не понадобиться, то можете смело удалять его со своего компьютера. Исходники всегда можно будет найти на этой странице github
 
## Удаленный сервер

Если вы не хотите запускать сервер на свой локальной машине, то можно пользоваться нашим (он развернут и запущен на ```185.236.22.74:50051```).

Если вы сами захотите поднять удаленный сервер (может быть потому что наш слишком слабый), то можно все также из корневой директории выполнить на удаленной машине:
```
docker-compose  up -d
```
Учтите, что база данных развертывается в контейнере, что не самое безопасное решение. Если хотите использовать свою базу данных, до достаточно сборки через ```make``` и изменения конфигов




# Клиент

Чтобы запустить клиента на своем компьютере, нужно склонировать этот репозиторий и поместить в клиентский конфиг следующие данные 


### Сервер запущен локально:
client/config.py:
```
host = "localhost"  # ip адрес сервера
port = "50051"  # слушающий порт сервера
```

### Сервер вне локальной сети
client/config.py:
```
host = "185.236.22.74"  # если хотите подключиться к нашему серверу. Иначе указываете свой ip
port = "50051"  #  если хотите подключиться к нашему серверу. Иначе указываете свой порт
```

Осталось подготовить клиент. Для этого выполните единожды 

```
make prepare_client
```

Теперь для запуска клиента достаточно выполнить 

```
make run_client
```

Также чтобы почистить клиент от созданных папок:
```
make clean_client
```

