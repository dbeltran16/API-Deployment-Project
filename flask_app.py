from migrations.instance.config import ProductionConfig, create_app

app = create_app(ProductionConfig)


@app.get("/")
def index() -> str:
    return "Flask app is running"


if __name__ == "__main__":
    app.run()

    