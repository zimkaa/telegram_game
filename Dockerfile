###########
# BUILDER #
###########
FROM python:3.11 as builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY ./pyproject.toml ./poetry.lock /app/

RUN pip install poetry && \
    poetry export -f requirements.txt --output requirements.txt --without-hashes --without dev && \
    pip install --no-cache-dir --upgrade -r requirements.txt

###########
## IMAGE ##
###########
FROM python:3.11-slim

WORKDIR /home/appuser/app

COPY . /home/appuser/app

RUN groupadd -r appgroup && useradd -r -g appgroup appuser

COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages

RUN chown -R appuser:appgroup /home/appuser/app

USER appuser

CMD ["./entrypoint.sh"]
