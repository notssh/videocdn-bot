# Установка

## Linux
В целом, на Windows процесс схож. Что конкретно делается на каждом этапе, я расписал.

1. Клонируйте этот репозиторий; перейдите в папку с проектом
```bash
git clone https://github.com/notssh/videocdn-bot/
cd videocdn-bot
```
2. Создайте Python-venv; активируйте его.
```bash
python3 -m venv venv
venv/bin/activate
```
3. Клонируйте репозиторий [videocdn-api](https://github.com/notssh/videocdn-api/); установите зависимости для этого модуля; вернитесь в директорию videocdn-bot.
```bash
git clone https://github.com/notssh/videocdn-api/
cd videocdn-api
pip3 install -r requirements.txt
```
4. Удалите ненужные файлы, переместите модуль videocdn-api на уровень выше.
```bash
rm README.md
rm requirements.txt
mv videocdn-api/* .
```
5. Установите зависимости для videocdn-bot:
```bash
pip3 install -r requirements_minimal.txt
```
Или так, если будете использовать аналитику и БД SQLite 
```bash
pip3 install -r requirements.txt
```
6. [Отредактируйте consts.py](https://github.com/notssh/videocdn-bot/docs/consts.md)
7. Запуск:
```bash
python3 main.py
```
