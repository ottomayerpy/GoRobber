# GoRobber
Онлайн мини игра

## Install

Клонируйте данный репозиторий и перейдите в каталог GoRobber.
```
git clone https://github.com/nikitakoltman/GoRobber
cd GoRobber
```
Создайте и активируйте виртуальное окружение python.
```
python3 -m venv env
source env/bin/activate
```
Установите зависимости.
```
pip install -r requirements.txt
```
Перейдите в директорию configs, создайте копию файла config-example.py с названием config.py и заполните
в нем нужные параметры (переменные из config.py импортируются в settings.py).
```
cd accounts/configs
cp config-example.py config.py
```
Перейдите обратно в директорию accounts и проведите миграции.
```
cd ..
python3 manage.py migrate
```
Создайте супер пользователя.
```
python3 manage.py createsuperuser
```
Активируйте сервер и пользуйтесь.
```
python3 manage.py runserver
```
