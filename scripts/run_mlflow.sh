#!/usr/bin/env bash

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MLFLOW_DIR="${PROJECT_DIR}/mlflow"
BACKEND_DIR="${MLFLOW_DIR}/backend"
ARTIFACTS_DIR="${MLFLOW_DIR}/artifacts"

HOST="0.0.0.0"
PORT="5000"

mkdir -p "${BACKEND_DIR}"
mkdir -p "${ARTIFACTS_DIR}"

echo "Project dir: ${PROJECT_DIR}"
echo "MLflow backend: ${BACKEND_DIR}"
echo "MLflow artifacts: ${ARTIFACTS_DIR}"

mlflow server \
  --backend-store-uri "sqlite:///${BACKEND_DIR}/mlflow.db" \
  --default-artifact-root "file://${ARTIFACTS_DIR}" \
  --host "${HOST}" \
  --port "${PORT}"
  