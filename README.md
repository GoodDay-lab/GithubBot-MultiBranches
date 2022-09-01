# Description

    Скрипт запускает простой сервер,
    который будет обрабатывать запросы с github-webhook
    и синхронизировать между собой репозитории.

### Названия веток, репозиториев и почтовых адресов - условны, вы можете заменить их.

# Installing

### ngrok
Для теста можно использовать ngrok.
После запуска появится интерактивное консольное окно, вам нужно поле Forwarding.
Оно представляет собой:  (ваше публичное url) -> (ваш локальный адрес). Вы копируете публичное url.

	   $ ngrok http 9999

Установить ngrok можно по этой ссылке на любую целевую систему (url) https://ngrok.com/download

### Install git and python packages
Утилита git должна быть в системной переменной PATH

Так же необходимо обеспечить автоаутенфикацию аккаунта (Советую использовать ssh):

       $ ssh-add ~/.ssh/yourprivatekey

Обязательно установить пакеты для python

	   $ python -m pip install -r requirements.txt

### Adding webhook
Перед началом надо подключить webhook

	- Заходите в свой репозиторий 
	- settings
	- webhook 
	- add a webhook 
	- "в поле url ставите url от ngrok"
	- Так же в параметры ssl надо установить "disable SSL".

Сервер не поддерживает протокол SSL.

# Usage

### to run:

        $ python main.py --config (configfile)

- config (configfile) - аргумент (configfile) - это путь к файлу, в котором будет                   храниться информация о репозиториях.


### Configure configfile
##### Текстовый файл, данные храняться в формате:
	
        [global]
        # Указывается ветка, которая обязательно должна находиться на
        # каждом репозитории, именно она будет синхронизироваться
        branch = main
        # Адрес за который программа будет 'цепляться'
        host = 127.0.0.1
        port = 9000
        # Директория с "временным" локальным репозиторием,
        # необходимым для более удобной передачи данных с удалённых репозиториев
        repository = /var/repository
        # Директория, в которой работает скрипт
        workdirectory = /var/repository

        # Названия секций всех репозиториев должны быть уникальны!
        # На их основе проводится идентификация удалённых репозиториев

        [repository1]
        # Параметры вашего первого репозитория
        url = git@github.com:...
        name = YourName
        email = YourEmail
        
        [repository2]
        # Параметры вашего второго репозитория
        url = git@github.com:...
        name = YourSecondName
        email = YourSecondEmail

### Examples

#### Example run script:
	$ python main.py --config ~/.config/multibranch.conf


