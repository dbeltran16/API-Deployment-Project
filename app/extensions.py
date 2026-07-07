from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# Shared extension instances for app factory pattern
db = SQLAlchemy()
migrate = Migrate()
