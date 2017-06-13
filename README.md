Used technologies: Django, Selenium, Celery
Used DB: PostgreSQL

RUN CELERY:
    celery --app=checkout_bot.celery:app worker --concurrency=1 --loglevel=info