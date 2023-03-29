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
 5. Откройте в браузере ссылку http://localhost:3000
    
    
   

## :fire: Пример работы


Результат обработки видео доступен [по ссылке](https://drive.google.com/file/d/1JQw0YGfoBiBzh3acKkAG37WcGMzoM_9h/view?usp=share_link)

<img align=center src='https://user-images.githubusercontent.com/51875349/228593390-0360c9ac-0519-464b-b4d6-bdae9a33dd04.png' width=400 height=250><img>
<img align=center src='https://user-images.githubusercontent.com/51875349/228594170-8f82ba56-33ac-49ea-b1ab-74ae4824f8b4.png' width=400 height=250><img>
