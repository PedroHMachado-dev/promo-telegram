import json
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

from storage import load_data, save_data


HOST = "127.0.0.1"
PORT = 8000


def slugify(value):
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "produto"


class ApiHandler(BaseHTTPRequestHandler):
    def _send_json(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "http://localhost:5173")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self):
        length = int(self.headers.get("Content-Length", "0"))
        return json.loads(self.rfile.read(length).decode("utf-8"))

    def do_OPTIONS(self):
        self._send_json(204, {})

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/api/dashboard":
            data = load_data()
            active_products = [p for p in data["products"] if p.get("active", True)]
            self._send_json(
                200,
                {
                    "products": active_products,
                    "groups": data["groups"],
                    "stats": {
                        "products": len(active_products),
                        "groups": len(data["groups"]),
                        "promotions": len(data["promotions"]),
                        "status": "online",
                    },
                    "recent_promotions": data["promotions"][-10:][::-1],
                },
            )
            return
        if path == "/api/health":
            self._send_json(200, {"status": "online"})
            return
        self._send_json(404, {"error": "Endpoint não encontrado"})

    def do_POST(self):
        path = urlparse(self.path).path
        if path == "/api/groups":
            self._create_group()
            return
        if path != "/api/products":
            self._send_json(404, {"error": "Endpoint não encontrado"})
            return
        try:
            payload = self._read_json()
            name = str(payload.get("name", "")).strip()
            max_price = float(payload.get("max_price", 0))
            if not name or max_price <= 0:
                raise ValueError("Nome e preço máximo são obrigatórios")

            data = load_data()
            base_id = slugify(name)
            used_ids = {product["id"] for product in data["products"]}
            product_id = base_id
            suffix = 2
            while product_id in used_ids:
                product_id = f"{base_id}-{suffix}"
                suffix += 1

            keywords = payload.get("keywords") or [name]
            if isinstance(keywords, str):
                keywords = [item.strip() for item in keywords.split(",") if item.strip()]

            product = {
                "id": product_id,
                "name": name,
                "description": str(payload.get("description", "")).strip() or name,
                "keywords": keywords,
                "max_price": max_price,
                "icon": str(payload.get("icon", "📦")),
                "active": True,
            }
            data["products"].append(product)
            save_data(data)
            self._send_json(201, product)
        except (ValueError, TypeError, json.JSONDecodeError) as error:
            self._send_json(400, {"error": str(error)})

    def _create_group(self):
        try:
            payload = self._read_json()
            name = str(payload.get("name", "")).strip()
            telegram_id = str(payload.get("id", "")).strip()
            if not name or not re.fullmatch(r"-?\d+", telegram_id):
                raise ValueError("Informe o nome e um ID numérico válido do Telegram")

            data = load_data()
            if any(str(group["id"]) == telegram_id for group in data["groups"]):
                raise ValueError("Este grupo já está cadastrado")

            group = {"id": telegram_id, "name": name, "active": True}
            data["groups"].append(group)
            save_data(data)
            self._send_json(201, group)
        except (ValueError, TypeError, json.JSONDecodeError) as error:
            self._send_json(400, {"error": str(error)})

    def do_DELETE(self):
        path = urlparse(self.path).path
        group_match = re.fullmatch(r"/api/groups/(-?\d+)", path)
        if group_match:
            self._delete_group(group_match.group(1))
            return

        match = re.fullmatch(r"/api/products/([^/]+)", path)
        if not match:
            self._send_json(404, {"error": "Endpoint não encontrado"})
            return

        product_id = match.group(1)
        data = load_data()
        original_length = len(data["products"])
        data["products"] = [p for p in data["products"] if p["id"] != product_id]
        if len(data["products"]) == original_length:
            self._send_json(404, {"error": "Produto não encontrado"})
            return
        save_data(data)
        self._send_json(200, {"deleted": product_id})

    def _delete_group(self, telegram_id):
        data = load_data()
        original_length = len(data["groups"])
        data["groups"] = [
            group for group in data["groups"] if str(group["id"]) != telegram_id
        ]
        if len(data["groups"]) == original_length:
            self._send_json(404, {"error": "Grupo não encontrado"})
            return
        save_data(data)
        self._send_json(200, {"deleted": telegram_id})

    def log_message(self, format, *args):
        print(f"[API] {self.address_string()} - {format % args}")


def run():
    server = ThreadingHTTPServer((HOST, PORT), ApiHandler)
    print(f"API disponível em http://{HOST}:{PORT}")
    print("Pressione CTRL+C para parar.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    run()
