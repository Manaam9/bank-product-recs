#!/usr/bin/env bash

set -e

# Настройки
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
IMAGE_NAME="bank-recs-api"
CONTAINER_NAME="bank-recs-api-container"
PORT=8000

echo "==============================="
echo "Starting API service via Docker"
echo "PROJECT_DIR: ${PROJECT_DIR}"
echo "IMAGE_NAME: ${IMAGE_NAME}"
echo "CONTAINER_NAME: ${CONTAINER_NAME}"
echo "PORT: ${PORT}"
echo "==============================="

cd "${PROJECT_DIR}"

# Останавливаем старый контейнер
if [ "$(docker ps -aq -f name=${CONTAINER_NAME})" ]; then
    echo "Stopping existing container..."
    docker stop ${CONTAINER_NAME} || true
    docker rm ${CONTAINER_NAME} || true
fi

# Сборка образа
echo "Building Docker image..."
docker build -t ${IMAGE_NAME} .

# Запуск контейнера
echo "Running container..."
docker run -d \
    --name ${CONTAINER_NAME} \
    -p ${PORT}:8000 \
    ${IMAGE_NAME}

echo "==============================="
echo "API is running at:"
echo "http://localhost:${PORT}"
echo "Swagger docs:"
echo "http://localhost:${PORT}/docs"
echo "==============================="
