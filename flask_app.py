import os

from app import create_app
from app.config import ProductionConfig

app = create_app(ProductionConfig)


@app.get("/")
def index() -> str:
    return "Flask app is running"


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)

