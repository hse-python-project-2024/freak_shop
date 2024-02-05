# Жуткая лавка
Адаптация настольной карточной игры о торговле страхом.

# Как запустить?

На сервере нужно создать базу данных, заполнить файл server/config.py, указав логин/пароль от юзера PostrgreSQL, название базы и хост

В приложении мы используем grpc запросы. Чтобы они корректно запускались, нужно скачать grpcio и grpcio-tools
(`python3 -m pip install grcpio grpcio-tools`). Чтобы сгенирировать proto файлы, нужно из корневой директории вызвать `python3 -m grpc_tools.protoc -I protos --python_out=. --grpc_python_out=. protos/db.proto`
