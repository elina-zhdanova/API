from flask import Blueprint, request
from flask_apispec import use_kwargs, marshal_with, doc
from werkzeug.exceptions import NotFound, BadRequest

from app.extensions import auth, docs
from app.services import URLService
from app.schemas import (
    URLSchema, URLListSchema, StatsSchema, CreateURLSchema
)

api_blueprint = Blueprint('api', __name__, url_prefix='/api/v1')

@api_blueprint.route('/shorten', methods=['POST'])
@auth.login_required
@doc(
    tags=['URL Management'],
    description='Create short URL',
    responses={
        201: {'description': 'Short URL created', 'schema': URLSchema},
        400: {'description': 'Invalid URL provided'}
    }
)
@use_kwargs(CreateURLSchema) #проверяет входные данные
@marshal_with(URLSchema, code=201) #Преобразует выходные данные в JSON по схеме
def shorten_url(**kwargs):
    # Если URL невалиден — автоматически вернёт 400 Bad Request
    return URLService.create_url(kwargs['original_url']), 201

@api_blueprint.route('/links', methods=['GET'])
@auth.login_required
@doc(
    tags=['URL Management'],
    description='List all URLs with pagination',
    responses={200: {'description': 'List of URLs', 'schema': URLListSchema}}
)
@marshal_with(URLListSchema)
def list_urls():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    active_only = request.args.get('active_only', 'true').lower() == 'true'
    
    pagination = URLService.get_paginated_urls(page, per_page, active_only)
    return {
        'items': pagination.items,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': pagination.page
    }

@api_blueprint.route('/links/<int:url_id>/deactivate', methods=['PUT'])
@auth.login_required
@doc(
    tags=['URL Management'],
    description='Deactivate URL',
    responses={
        204: {'description': 'URL deactivated'},
        404: {'description': 'URL not found'}
    }
)
def deactivate_url(url_id):
    if not URLService.deactivate_url(url_id):
        raise NotFound('URL not found')
    return '', 204

@api_blueprint.route('/stats', methods=['GET'])
@auth.login_required
@doc(
    tags=['Statistics'],
    description='Get visit statistics',
    responses={200: {'description': 'Visit statistics', 'schema': StatsSchema}}
)
@marshal_with(StatsSchema)
def get_stats():
    return {'items': URLService.get_stats()}

# Регистрация документации
docs.register(shorten_url, blueprint='api')
docs.register(list_urls, blueprint='api')
docs.register(deactivate_url, blueprint='api')
docs.register(get_stats, blueprint='api')