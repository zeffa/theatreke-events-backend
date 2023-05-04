FROM python:3.9.6-alpine

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PROJECT_DIR /events

WORKDIR $PROJECT_DIR

RUN addgroup -S admin && adduser -S admin -G admin

RUN apk update && apk add postgresql-development gcc python3-development musl-development

RUN pip install --upgrade pip

RUN pip install pipenv

COPY scripts /scripts

RUN chmod +x /scripts/*

COPY theatreevents $PROJECT_DIR

COPY Pipfile Pipfile.lock $PROJECT_DIR

RUN chown -R admin:admin $PROJECT_DIR

RUN chmod -R 755 $PROJECT_DIR

RUN pipenv install --system --development

USER admin

#CMD ["/scripts/run.sh"]