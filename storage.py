import json
import os
import tempfile
import threading
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path


DATA_FILE = Path(__file__).resolve().parent / "data" / "app_data.json"
_LOCK = threading.RLock()

DEFAULT_DATA = {
    "products": [
        {
            "id": "monitor-lg-ultragear-32gn600",
            "name": "Monitor LG Ultragear 32GN600",
            "description": "Monitor 32 polegadas QHD 165Hz",
            "keywords": ["lg ultragear 32gn600", "32gn600", "32gn600-32"],
            "max_price": 1000.0,
            "icon": "🖥️",
            "active": True,
        },
        {
            "id": "iphone-15",
            "name": "iPhone 15",
            "description": "Apple iPhone 15",
            "keywords": ["iphone 15", "iphone15"],
            "max_price": 3000.0,
            "icon": "📱",
            "active": True,
        },
        {
            "id": "ps5",
            "name": "PS5",
            "description": "Console PlayStation 5",
            "keywords": ["playstation 5", "playstation5", "ps5"],
            "max_price": 3500.0,
            "icon": "🎮",
            "active": True,
        },
    ],
    "groups": [],
    "telegram_groups": [],
    "telegram_groups_updated_at": None,
    "promotions": [],
}


def _ensure_file():
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not DATA_FILE.exists():
        _write_unlocked(DEFAULT_DATA)


def _write_unlocked(data):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(
        dir=str(DATA_FILE.parent), prefix="app_data_", suffix=".json"
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
            file.write("\n")
        os.replace(temp_name, DATA_FILE)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def load_data():
    with _LOCK:
        _ensure_file()
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
        data.setdefault("products", [])
        data.setdefault("groups", [])
        data.setdefault("telegram_groups", [])
        data.setdefault("telegram_groups_updated_at", None)
        data.setdefault("promotions", [])
        return data


def save_data(data):
    with _LOCK:
        _write_unlocked(data)
        return deepcopy(data)


def products_for_filters():
    products = load_data()["products"]
    return {
        product["name"]: {
            "palavras_chave": product["keywords"],
            "preco_maximo": float(product["max_price"]),
        }
        for product in products
        if product.get("active", True)
    }


def add_promotion(product, previous_price, current_price, savings, discount, link):
    with _LOCK:
        data = load_data()
        data["promotions"].append(
            {
                "id": f"promotion-{len(data['promotions']) + 1}",
                "product": product,
                "previous_price": previous_price,
                "current_price": current_price,
                "savings": savings,
                "discount": discount,
                "link": link,
                "created_at": datetime.now(timezone.utc).isoformat(),
            }
        )
        _write_unlocked(data)


def save_telegram_groups(groups):
    with _LOCK:
        data = load_data()
        data["telegram_groups"] = groups
        data["telegram_groups_updated_at"] = datetime.now(timezone.utc).isoformat()
        _write_unlocked(data)
