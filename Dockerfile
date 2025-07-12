FROM python:3.13-alpine3.21

WORKDIR /app

RUN apk update \
    && apk add --no-cache libpq-dev gcc musl-dev

RUN addgroup -S appgroup && \
    adduser -S appuser -G appgroup

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ERPDjangoProject ERPDjangoProject
COPY start.sh .
RUN chmod +x start.sh

RUN chown -R appuser:appgroup /app

USER appuser

ENTRYPOINT ["sh", "start.sh"]
CMD ["python","ERPDjangoProject/manage.py","runserver","0.0.0.0:8000"]
