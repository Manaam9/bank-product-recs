#!/usr/bin/env bash

set -e

# Пути проекта
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MLFLOW_DIR="${PROJECT_DIR}/mlflow"
ARTIFACTS_DIR="${MLFLOW_DIR}/artifacts"

# Настройки сервера
HOST="0.0.0.0"
PORT="5001"

# Подготовка директорий
mkdir -p "${MLFLOW_DIR}"
mkdir -p "${ARTIFACTS_DIR}"

# Пути MLflow
BACKEND_URI="sqlite:///${MLFLOW_DIR}/mlflow.db"
ARTIFACT_URI="file://${ARTIFACTS_DIR}"

# Логи
echo "==============================="
echo "MLflow server configuration"
echo "PROJECT_DIR: ${PROJECT_DIR}"
echo "MLFLOW_DIR: ${MLFLOW_DIR}"
echo "BACKEND_URI: ${BACKEND_URI}"
echo "ARTIFACT_URI: ${ARTIFACT_URI}"
echo "HOST: ${HOST}"
echo "PORT: ${PORT}"
echo "==============================="

# Запуск MLflow
mlflow server \
  --backend-store-uri "${BACKEND_URI}" \
  --default-artifact-root "${ARTIFACT_URI}" \
  --host "${HOST}" \
  --port "${PORT}"
