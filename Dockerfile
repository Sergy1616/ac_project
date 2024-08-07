FROM python:3.9-alpine3.19

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1

WORKDIR /ac_app
EXPOSE 8000
RUN apk add --no-cache postgresql-client build-base postgresql-dev
COPY requirements.txt /temp/requirements.txt
RUN pip install -r /temp/requirements.txt
RUN adduser --disabled-password ac-user

COPY entrypoint.sh /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

USER ac-user
COPY ac_app /ac_app

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]