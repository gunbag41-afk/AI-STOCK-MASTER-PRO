FROM python:3.12-slim
WORKDIR /app
COPY index.html server.py ./
ENV PYTHONUNBUFFERED=1
CMD ["python", "server.py"]
