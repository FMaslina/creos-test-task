<h1>Тестовое задание на позицию Python Developer в компании CREOS Play</h1>
<h2>Инструкция по установке и запуску</h2>
<h3>Вручную</h3>
<ol>
<li>Склонировать репозиторий через команду "git clone https://github.com/FMaslina/creos-test-task.git"</li>
<li>Установить зависимости через команду "pip install -r requirements.txt"</li>
<li>Провести миграции через команду "python manage.py migrate"</li>
<li>Запустить сервис командой "python manage.py runserver"</li>
<li><li>Запустить бота командой "python manage.py bot"</li></li>
<li>Зайти на запустившийся локальный сервер по адресу "127.0.0.1:8000"</li>
</ol>
<h3>Через docker</h3>
<ol>
<li>Запустить команду docker-compose up --build</li>
</ol>
<h3>Список эндпоинтов</h3>
<ol>
<li>"api/v1/weather" - Получение погоды по городу</li>
<ul>
Список возможных Query-параметров:
<li>city(str) - название города</li>
</ul>
<li>"api/v1/requests" - Получение истории запросов
<ul>
Список возможных Query-параметров:
<li>page(int) - страница в пагинации</li>
<li>page_size(int) - стандартно 10, количество объектов на странице, максимум 100</li>
<li>ordering(str) - сортировка по полю(city_name или created_at)</li>
<li>request_type(str) - фильтрация по типу запроса (web или telegram)</li>
</ul>
</li>


</ol>

<h2>Переменные окружения</h2>
<p>В корневой папке проекта есть .env.example файл с примером необходимых
данных для работы приложения</p>
