# videocdn-bot
Telegram-бот для поиска контента на videocdn.tv.

[@vcdntvbot](https://t.me/vcdntvbot)

## Features
- Поддерживает [инлайн-режим](https://core.telegram.org/bots/inline).
- Быстрый поиск по команде /search и дальнейшая навигация с помощью инлайн-кнопок в сообщении.
- Асинхронный (aiogram, aiohttp, sqlalchemy)
- Поддерживает сбор "статистики" (количество использования /start, /search и инлайна каждым пользователем), поддерживаются различные DB (библиотека sqlalchemy).

## Используемые библиотеки:
- aiogram 2
- sqlalchemy
- [videocdn-api](https://github.com/notssh/videocdn-api/)

## Установка и настройка
- [Читать здесь](https://github.com/notssh/videocdn-bot/blob/main/docs/install.md)

## TODO
- Более качественная обработка исключений
- Немного перенастроить логгирование
- Возможно, кэширование?..
- ???
