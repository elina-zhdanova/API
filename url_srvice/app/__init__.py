from flask import Flask
from flask_migrate import Migrate

def create_app(config_class='app.config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from app.extensions import db, auth, docs
    db.init_app(app)
    migrate = Migrate(app, db)

    from app.views.api import api_blueprint
    from app.views.redirect import redirect_blueprint
    app.register_blueprint(api_blueprint)
    app.register_blueprint(redirect_blueprint)

    docs.init_app(app)
    register_schemas(docs)

    return app

def register_schemas(docs):
    from app.schemas import (
        URLSchema, URLListSchema, StatsSchema, CreateURLSchema
    )
    
    # Регистрация схем
    docs.spec.components.schema("URL", schema=URLSchema)
    docs.spec.components.schema("URLList", schema=URLListSchema)
    docs.spec.components.schema("Stats", schema=StatsSchema)
    docs.spec.components.schema("CreateURL", schema=CreateURLSchema)

    # Добавляем поддержку Basic Auth
    docs.spec.components.security_scheme(
        "basic_auth",
        {
            "type": "http",
            "scheme": "basic",
            "description": "Введите логин и пароль администратора"
        }
    )
    
    # Применяем авторизацию ко всем эндпоинтам
    docs.spec.options["security"] = [{"basic_auth": []}]