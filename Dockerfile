FROM python:3.9.6-alpine

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PROJECT_DIR /events

WORKDIR $PROJECT_DIR

RUN addgroup -S admin && adduser -S admin -G admin

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install --upgrade pip

RUN pip install pipenv

COPY scripts /scripts

RUN chmod +x /scripts/*

COPY theatre-events $PROJECT_DIR

RUN mkdir -p /vol/web/static

COPY Pipfile Pipfile.lock $PROJECT_DIR

RUN chown -R admin:admin $PROJECT_DIR

RUN chown -R admin:admin /vol

RUN chown -R 755 /vol/web

RUN cd $PROJECT_DIR && pipenv install --system --dev

USER admin

CMD ["scripts/run.sh"]