FROM python:3.13-alpine3.21

WORKDIR /app

RUN apk update \
    && apk add --no-cache libpq-dev gcc musl-dev

RUN addgroup -S appgroup && \
    adduser -S appuser -G appgroup

COPY ERPDjangoProject/requirements.txt .
RUN pip install -r requirements.txt
COPY ERPDjangoProject/ .
RUN chmod +x start.sh

RUN chown -R appuser:appgroup /app

USER appuser

ENTRYPOINT ["sh", "start.sh"]
CMD ["python","manage.py","runserver","0.0.0.0:8000"]
