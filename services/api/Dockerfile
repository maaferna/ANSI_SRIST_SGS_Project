FROM python:3.11-slim

WORKDIR /app

COPY services/api/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY services/api/app/ /app/app
COPY infra/scripts/entrypoint_api.sh /app/entrypoint_api.sh
RUN chmod +x /app/entrypoint_api.sh

EXPOSE 8080
CMD ["/app/entrypoint_api.sh"]
