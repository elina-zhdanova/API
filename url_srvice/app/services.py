import string
import secrets
from datetime import datetime, timedelta, timezone
from app.extensions import db
from app.models import URLMap
from app.config import Config

class URLService:
    @staticmethod
    def generate_short_url():
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(Config.SHORT_URL_LENGTH))

    @staticmethod
    def create_url(original_url):
        short_url = URLService.generate_short_url()
        while URLMap.query.filter_by(short_url=short_url).first():  #эквивалентно SELECT * FROM url_map WHERE short_url = 'значение_short_url' LIMIT 1;
            short_url = URLService.generate_short_url()
        
        url = URLMap(
            original_url=original_url,
            short_url=short_url
        )
        db.session.add(url)
        db.session.commit()
        return url

    @staticmethod
    def get_url(short_url):
        return URLMap.query.filter_by(short_url=short_url).first()

    @staticmethod
    def deactivate_url(url_id):
        url = URLMap.query.get(url_id)
        if url:
            url.is_active = False
            db.session.commit()
        return url

    @staticmethod
    def get_paginated_urls(page=1, per_page=10, active_only=True):
        query = URLMap.query.order_by(URLMap.created_at.desc())
        if active_only:
            query = query.filter_by(is_active=True)
        return query.paginate(page=page, per_page=per_page, error_out=False)

    @staticmethod
    def get_stats():
        return URLMap.query.order_by(URLMap.visits.desc()).all()

    @staticmethod
    def register_visit(url):
        url.visits += 1
        url.last_accessed = datetime.now(timezone.utc)
        db.session.commit() 