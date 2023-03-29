## :page_facing_up: Описание

Вебсервисное приложение, использующее технологии глубокого обучения для аудиосопровождения происходящего на экране для людей с нарушением зрения.

## :mag: Инструкция 

1. Перейдите в папку ... выполните команду ```python -m venv venv```
2. Активируйте виртуальное окружение 
  - ```venv/bin/activate``` для Linux
  - ```venv/Scripts/Activate.ps1``` для Windows
3. Установите необходимые зависимости ```pip install -r requirements.txt```
4. Запуск пригриложения
  - Frontend:
    - Перейдите в папку "frontend".
    - Создайте файл .env.local и напишите в нем SERVER='http://localhost:XXXX'.
    - Запустите команду ```npm i```.
    - Выполните команду ```npm run dev```.
  - Backend:
    - Перейдите в папку "backend".
    - Coздайте папку data.
    - Cоздайте файл .env, где напишите STORAGE = 'data'.
    - Выполните команду ```python app.py```
    
    
   

## :fire: Пример работы

Результат обработки видео доступен [по ссылке](https://drive.google.com/file/d/1JQw0YGfoBiBzh3acKkAG37WcGMzoM_9h/view?usp=share_link)
