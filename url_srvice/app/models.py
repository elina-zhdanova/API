from datetime import datetime, timedelta
from app.extensions import db
from app.config import Config
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

from datetime import datetime, timedelta, timezone

class URLMap(db.Model):
    __tablename__ = 'url_maps'
    
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(2048), nullable=False)
    short_url = db.Column(db.String(Config.SHORT_URL_LENGTH), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    expires_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc) + timedelta(days=Config.URL_EXPIRATION_DAYS)
    )
    is_active = db.Column(db.Boolean, default=True)
    visits = db.Column(db.Integer, default=0)
    last_accessed = db.Column(db.DateTime)
    
    def is_expired(self):
        return datetime.now(timezone.utc) > self.expires_at
    
    # Преобразование объекта в словарь для API
    def to_dict(self):
        return {
            'id': self.id,
            'original_url': self.original_url,
            'short_url': self.short_url,
            'created_at': self.created_at.isoformat(), #ISO 8601 — международный стандарт представления даты и времени, нужно для JSON
            'expires_at': self.expires_at.isoformat(),
            'is_active': self.is_active,
            'visits': self.visits
        }