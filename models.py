from marshmallow import Schema, fields, validate

class User:
    def __init__(self, id, full_name, cpf, email, balance):
        self.id = id
        self.full_name = full_name
        self.cpf = cpf
        self.email = email
        self.balance = balance

    def serialize(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'cpf': self.cpf,
            'email': self.email,
            'balance': self.balance
        }
    
class NewUserSchema(Schema):
    full_name = fields.String(required=True, validate=validate.Length(min=2) , error_messages={'required': "Required field", 'invalid': "Invalid field"})
    cpf = fields.String(required=True, validate=validate.Length(min=11,max=11), error_messages={'required': "Required field", 'invalid': "Invalid field"})
    email = fields.Email(required=True, error_messages={'required': "Required field", 'invalid': "Invalid field"})
    balance = fields.Float(required=True, error_messages={'invalid': "Invalid field"})

class UpdateUserSchema(Schema):
    id = fields.Integer(required=True, error_messages={'required': "Required field", 'invalid': "Invalid field"})
    full_name = fields.String(required=False, validate=validate.Length(min=2) , error_messages={'required': "Required field", 'invalid': "Invalid field"})
    cpf = fields.String(required=False, validate=validate.Length(min=11,max=11), error_messages={'required': "Required field", 'invalid': "Invalid field"})
    email = fields.Email(required=False, error_messages={'required': "Required field", 'invalid': "Invalid field"})
    balance = fields.Float(required=False, error_messages={'invalid': "Invalid field"})

class TransactionSchema(Schema):
    payer_id = fields.Integer(required=True, error_messages={'required': "Required field", 'invalid': "Invalid field"})
    payee_id = fields.Integer(required=True, error_messages={'required': "Required field", 'invalid': "Invalid field"})
    amount = fields.Integer(required=True, error_messages={'required': "Required field", 'invalid': "Invalid field"})