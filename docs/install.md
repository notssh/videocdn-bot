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
source venv/bin/activate
```
3. Клонируйте репозиторий [videocdn-api](https://github.com/notssh/videocdn-api/); установите зависимости для этого модуля;
```bash
git clone https://github.com/notssh/videocdn-api/
cd videocdn-api
pip3 install -r requirements.txt
```
4. Удалите ненужные файлы, переместите модуль videocdn_api в директорию с ботом (в данном случае - на уровень выше); вернитесь в директорию с ботом;
```bash
rm README.md
rm requirements.txt
mv videocdn_api ../
cd ..
```
5. Установите зависимости для videocdn-bot:
```bash
pip3 install -r requirements_minimal.txt
```
Или так, если будете использовать аналитику и БД SQLite (будут также установлены aiosqlite и sqlalchemy) 
```bash
pip3 install -r requirements_sqlite.txt
```
[Важная деталь насчет БД](https://github.com/notssh/videocdn-bot/blob/main/docs/db.md)  
6. [Отредактируйте consts.py](https://github.com/notssh/videocdn-bot/blob/main/docs/consts.md)  
7. Запуск:
```bash
python3 main.py
```

Внимание! Должны существовать полные пути до логов и базы данных, со всеми поддиректориями! Иначе выдаст ошибку FileNotFoundError: [Errno 2] No such file or directory.
