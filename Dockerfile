FROM python:3.11.5-bookworm AS app

WORKDIR /app

ARG UID=1000
ARG GID=1000

RUN apt-get update \
  && apt-get install -y --no-install-recommends build-essential curl libpq-dev nano \
  && rm -rf /var/lib/apt/lists/* /usr/share/doc /usr/share/man \
  && apt-get clean \
  && groupadd -g "${GID}" python \
  && useradd --create-home --no-log-init -u "${UID}" -g "${GID}" python \
  && pip install --upgrade pip

USER python

COPY --chown=python:python requirements*.txt ./
RUN pip install -r requirements.txt

ARG DEBUG="false"
ENV DEBUG="${DEBUG}" \
    PYTHONDONTWRITEBYTECODE="true" \
    PYTHONUNBUFFERED="true" \
    PYTHONPATH="." \
    PATH="${PATH}:/home/python/.local/bin" \
    USER="python"

COPY --chown=python:python ./src .

USER root

COPY ./scripts/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./scripts/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY ./scripts/worker /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker

COPY ./scripts/scheduler /start-cron
RUN sed -i 's/\r$//g' /start-cron
RUN chmod +x /start-cron

USER python

WORKDIR /app

EXPOSE 5000

ENTRYPOINT ["/entrypoint"]


