Used technologies: Django, Selenium, Celery
Used DB: PostgreSQL

RUN CELERY:
    celery --app=checkout_bot.celery:app worker --concurrency=1 --loglevel=info

DEPLOYMENT:
	git clone https://github.com/alexeykuz/checkout_bot.git

	sudo apt-get install virtualenv
	sudo add-apt-repository ppa:fkrull/deadsnakes
	sudo apt-get update
	sudo apt-get install python2.7
	export LC_ALL=C
	cd checkout_bot/
	virtualenv --python=/usr/bin/python2.7 .env
	. .env/bin/activate
	pip install -r requirements.txt

	deactivate

	sudo apt-get install supervisor
	sudo apt-get install nginx

	cd checkout_bot/conf/
	sudo cp nginx_checkout_bot.conf /etc/nginx/sites-available/nginx_checkout_bot.conf
	sudo ln /etc/nginx/sites-available/nginx_checkout_bot.conf /etc/nginx/sites-enabled/nginx_checkout_bot.conf
	sudo cp celery.conf /etc/supervisor/conf.d/celery.conf
	sudo cp checkout_django.conf /etc/supervisor/conf.d/checkout_django.conf
	sudo cp display.conf /etc/supervisor/conf.d/display.conf

	sudo apt-get install postgresql postgresql-contrib
	sudo -i -u postgres
	psql
	create database db;
	CREATE USER user WITH PASSWORD 'pswrd';
	GRANT ALL PRIVILEGES ON DATABASE db to user;

	ctrl+d

	add settings_local.py
	mkdir logs

	./manage.py migrate
	./manage.py createsuperuser

	sudo apt-get install gunicorn
	sudo apt-get install xvfb

	wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add - 
	sudo sh -c 'echo "deb https://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
	sudo apt-get update
	sudo apt-get install google-chrome-stable

	pip install gunicorn

	nano /home/ubuntu/gunicorn.conf.py
	add to file:
		bind = '127.0.0.1:8001'
		workers = 1

	wget -O- https://www.rabbitmq.com/rabbitmq-release-signing-key.asc | sudo apt-key add -
	sudo apt-get update
	sudo apt-get install rabbitmq-server

	sudo apt-get install build-essential autoconf libtool pkg-config python-opengl python-imaging python-pyrex python-pyside.qtopengl idle-python2.7 qt4-dev-tools qt4-designer libqtgui4 libqtcore4 libqt4-xml libqt4-test libqt4-script libqt4-network libqt4-dbus python-qt4 python-qt4-gl libgle3 python-dev libssl-dev

	add rule to security groups to enable 8000 port

	sudo service supervisor restart
	sudo service nginx restart
