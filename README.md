# Description
- Скрипт запускает простой сервер,
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
	$ python main.py --host (host) --port (port) --localrepo (path to localrepo) --config (path to config file)

- localrepo (localrepo) - аргумент (localrepo) - это путь к папке, которая будет создана для связывания всех репозиториев в единое целое. После окончания работы скрипта должна автоматически удалиться, если указывает на существующую папку, то сначала удаляет её, даже, если она не пустая, будьте аккуратны (WARNING!!!)

- config (configfile) - аргумент (configfile) - это путь к файлу, в котором будет храниться информация о репозиториях.
	
- host (host) - аргумент (host) - это хост на котором будет работать скрипт. Доменное имя или IP адрес, например, "localhost". 

- port (port) - порт, на котором будет работать скрипт. Должно быть числом от 2^0 до 2^16 (65355, включительно) 


### Configure configfile
##### Текстовый файл, данные храняться в формате:
	
        '''
        [global]
        # Указывается ветка, которая обязательно должна находиться на
        # каждом репозитории, именно она будет синхронизироваться
        branch = main

        # Названия секций всех репозиториев должны быть уникальны!

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
        '''

### Examples

#### Example run script:
	$ python main.py --localrepo ~/localrepo --config ./config


