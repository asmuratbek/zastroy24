# [Python/Django] MyBrands

Запуск Django приложения:

  * Склонируйте репозиторий в нужную вам директорию `git clone https://bitbucket.org/kiritoart95/my_brands`
  * Откройте проект используя PyCharm или другие IDE
  * Перейдите в директорию `\MyBrands`
  * Создайте в этой директории файл `parameters.py`
  * Скопируйте в неё содержание файла `parameters.py.dist`
  * Произведите настройку проекта в файле `parameters.py` по своему усмотрению
  * Зайдите в базу данных, и содайте там базу (Помните, название базы длжно совпадать с названием, которе вы ставили в `parameters.py`)
  * Создайте и активирйте системное окружение `~$ virtualenv ../my_brands_env` и `~$ source ../my_brands_env/bin/activate`
  * Установите все необходимые библеотеки `(my_brands_env) ~$ pip install -r req.txt`
  * Промигрируйте базу командой `(my_brands_env) ~$ python manage.py migrate`
  * Установите все статические файлы `(my_brands_env) ~$ python manage.py collectstatic`
  * После создайте супер админа коммандой `(my_brands_env) ~$ python manage.py createsuperuser`
  * После можете запустить сервер командой `(my_brands_env) ~$ python manage.py runserver 8000`

Теперь перйдите на [`localhost:8000`](http://localhost:8000) в вашем браузере, чтобы убедится, что всё работает.

## Статичесие файлы

  * Все статические файлы хранятся в директории по пути `\templates\public\`
  * Шрифты для водного знака находятся в `\Meta\etc\`
  * Чтобы применить новый загруженный шрифт перейдите в `\MyBrands\settings.py` и измените в нём строчку:
      
        WATERMARK_FONT = os.path.join(BASE_DIR, 'Meta', 'etc', 'calibrib.ttf')
        
## Шаблоны HTML

  * Все HTML, нужные для сайта, хранятся в директории `\templates\app` и `\templates\account`
