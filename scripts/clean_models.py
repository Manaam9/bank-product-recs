#!/usr/bin/env python3

from pathlib import Path

# Пути проекта
CURRENT_DIR = Path.cwd().resolve()

if CURRENT_DIR.name == "scripts":
    PROJECT_ROOT = CURRENT_DIR.parent
else:
    PROJECT_ROOT = CURRENT_DIR

MODELS_DIR = PROJECT_ROOT / "models"

# Базовые файлы
FILES_TO_DELETE = [
    MODELS_DIR / "als_model.pkl",
    MODELS_DIR / "user_item_matrix.npz",
    MODELS_DIR / "user2idx.pkl",
    MODELS_DIR / "item2idx.pkl",
    MODELS_DIR / "idx2item.pkl",
]

deleted = 0

print("=== Cleaning base files ===")
for path in FILES_TO_DELETE:
    if path.exists():
        path.unlink()
        print(f"Deleted: {path}")
        deleted += 1
    else:
        print(f"Not found: {path}")

# Удаляем все .bin модели
print("\n=== Cleaning .bin models ===")
for path in MODELS_DIR.glob("*.bin"):
    path.unlink()
    print(f"Deleted: {path}")
    deleted += 1

# Удаляем OVR директорию (если есть)
OVR_DIR = MODELS_DIR / "ovr"

if OVR_DIR.exists():
    print("\n=== Cleaning OVR directory ===")
    for file in OVR_DIR.glob("*"):
        file.unlink()
        print(f"Deleted: {file}")
        deleted += 1

    OVR_DIR.rmdir()
    print(f"Removed directory: {OVR_DIR}")

# Итог
print(f"\nDone. Total deleted files: {deleted}")
