from marshmallow import Schema, fields, ValidationError

class UserSchema(Schema):
    name = fields.Str(required=True, validate=lambda x: len(x) >= 2)
    email = fields.Email(required=True)

# Validate request data
def validate_user_data(data):
    schema = UserSchema()
    try:
        result = schema.load(data)
        return True, result
    except ValidationError as err:
        return False, err.messages