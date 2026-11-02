FROM python:3.12-slim
WORKDIR /app
COPY index.html server.py ./
ENV PORT=8765 PYTHONUNBUFFERED=1
EXPOSE 8765
CMD ["python", "server.py"]
