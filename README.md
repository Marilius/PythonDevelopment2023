# PythonDevelopment2023

# CHESS # 
---

### build, install, and run

Нужен pipenv и python3.10

```
$ pipenv install
$ pipenv shell # теперь вы в виртуальном окружении
$ flake8 # чекнуть кодстайл
$ doit test # запуск юнит тестов (их пока нет)
$ doit whlclient # создание .whl для клиента
$ pip install --force-reinstall .\client\dist\Chess_client-0.0.1-py3-none-any.whl # установка клиента и всех зависимостей из .whl файла, --force-reinstall т.к. версию редачить лень, а pip за этим следит и думает, что пакет уже стоит. Также установка из файла должна работать в чистом виртуальном окружении
$ сhess-client # запуск клиента (точка входа в __main__.py:run)
```
TODO(marilius)

---
### Постановка задачи(неформально):

Разработать приложение, позволяющее:
+ режим хотсит
+ создание комнаты для игры по сети
+ подключение к комнате и игра по сети
+ (опционально) экспорт шахматной партии
+ (очень опционально) бот для оффлайн игры

---
### Участники

[Басалов Ярослав Александрович](https://github.com/Marilius)

[Гриненко Анна Андреевна](https://github.com/VeryLittleAnna)

[Епифанова Агата Станиславовна]()

---
### Макет:

TODO(marilius)
