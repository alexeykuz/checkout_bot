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
	virtualenv --python=/usr/bin/python2.7 .env
	pip install -r requirements.txt
	sudo apt-get install supervisor
	sudo apt-get install nginx
