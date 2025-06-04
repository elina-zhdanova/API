from marshmallow import Schema, fields, validate

class URLSchema(Schema):
    id = fields.Int(dump_only=True)
    original_url = fields.Str(required=True)
    short_url = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    expires_at = fields.DateTime(dump_only=True)
    is_active = fields.Boolean(dump_only=True)
    visits = fields.Int(dump_only=True)

#список URL с пагинацией
class URLListSchema(Schema):
    items = fields.List(fields.Nested(URLSchema))
    total = fields.Int()
    pages = fields.Int()
    current_page = fields.Int()

class StatsSchema(Schema):
    items = fields.List(fields.Nested(URLSchema))

#проверяет, что передан валидный URL
class CreateURLSchema(Schema):
    original_url = fields.Str(
        required=True,
        validate=validate.URL(relative=False, error="Invalid URL format")
    )