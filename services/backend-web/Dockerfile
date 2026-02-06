FROM mambaorg/micromamba:1.5.10

WORKDIR /app

# Copy env spec + requirements (from repo root)
COPY --chown=$MAMBA_USER:$MAMBA_USER services/backend-web/environment.yml /app/environment.yml
COPY --chown=$MAMBA_USER:$MAMBA_USER services/backend-web/requirements.txt /app/requirements.txt

# Create conda env (pip reads requirements.txt from image)
RUN micromamba create -y -n web -f /app/environment.yml && micromamba clean -a -y

ENV MAMBA_DOCKERFILE_ACTIVATE=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy Django source (from repo root)
COPY --chown=$MAMBA_USER:$MAMBA_USER services/backend-web/src/ /app/src/

# Copy entrypoint from centralized infra
COPY --chown=$MAMBA_USER:$MAMBA_USER infra/scripts/entrypoint_web.sh /app/entrypoint_web.sh
RUN chmod +x /app/entrypoint_web.sh


# Crear carpeta de staticfiles y asegurar permisos
RUN mkdir -p /app/src/staticfiles \
    && chown -R mambauser:mambauser /app/src

WORKDIR /app/src
EXPOSE 8001
CMD ["/app/entrypoint_web.sh"]
