from flask import Blueprint, redirect
from werkzeug.exceptions import NotFound

from app.services import URLService

redirect_blueprint = Blueprint('redirect', __name__)

@redirect_blueprint.route('/')
def home():
    return "Welcome to URL Shortener Service. Use /api/v1/shorten to create short URLs."

@redirect_blueprint.route('/<short_url>')
def redirect_to_original(short_url):
    url = URLService.get_url(short_url)
    
    if not url or not url.is_active or url.is_expired():
        raise NotFound('URL not found or expired')
    
    URLService.register_visit(url)
    return redirect(url.original_url, code=302)