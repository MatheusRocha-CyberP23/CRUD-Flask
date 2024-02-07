from flask import Flask, request, jsonify
from models import User, NewUserSchema, UpdateUserSchema, TransactionSchema
from marshmallow import ValidationError
import db, os

app = Flask(__name__)

def initialize_db():
    if not os.path.isfile('users.db'):
        db.connect()

@app.route("/user/add", methods=['POST'])
def add_user():
    req_data = request.get_json()
    schema = NewUserSchema() 

    try:     
        data = schema.load(req_data)
    except ValidationError as err:
        return jsonify(status='422', res='failure', error=err.messages) 
       
    users = [user.serialize() for user in db.view()]
    for user in users:
        if user['cpf'] == data['cpf'] or user['email'] == data['email']:
            return jsonify(res=f'Error! User is already registered!', status='404')
        
    user = User(db.get_new_id(), data['full_name'], data['cpf'], data['email'], data['balance'])    
    db.insert(user)      
    return jsonify(response=user.serialize(), status='200', msg='Success creating a new user!')

@app.route('/user/request', methods=['GET'])
def get_users():
    users = [user.serialize() for user in db.view()]
    return jsonify(response=users, status='200', msg='Success getting all users!', no_of_users=len(users))

@app.route('/user/request/<id>', methods=['GET'])
def get_user_by_id(id):
    user = db.get_user_by_id(id)
    if user:
        return jsonify(res=user, status='200', msg='Success getting user by ID!')
    return jsonify(error=f"Error! user with id '{id}' was not found!", status='404')

@app.route("/user/update", methods=['PUT'])
def update_user():
    req_data = request.get_json()
    schema = UpdateUserSchema()  
    
    try:     
        data = schema.load(req_data)
    except ValidationError as err:
        return jsonify(status='422', res='failure', error=err.messages)
    
    user = db.get_user_by_id(data['id'])
    if user:
        if 'email' in data:
            existing_user = db.get_user_by_email(data['email'])
            if existing_user and existing_user['id'] != user['id']:
                return jsonify(res=f'Error! Email {data["email"]} already exists.', status='400')
        if 'cpf' in data:
            existing_user = db.get_user_by_cpf(data['cpf'])
            if existing_user and existing_user['id'] != user['id']:
                return jsonify(res=f'Error! CPF {data["cpf"]} already exists.', status='400')

        for field in schema.fields:
            if field in data and field != 'id':               
                user[field] = data[field]
        
        update_user = User(data['id'], user['full_name'], user['cpf'], user['email'], user['balance'])     
        db.update(update_user)           
        return jsonify(res=update_user.serialize(), status='200', msg=f'Success updating the user: {update_user.full_name}!')
    return jsonify(res=f'Error! Failed to update user with id: {id}', status='404')

@app.route('/user/delete/<id>', methods=['DELETE'])
def delete_user(id):
    user = db.get_user_by_id(id)
    if user:
        db.delete(user['id'])
        updated_users = [user.serialize() for user in db.view()]              
        return jsonify(res=updated_users, status='200', msg='Success deleting user by ID!', no_of_users=len(updated_users))
    return jsonify(error=f"Error! user with id '{id}' was not found!", status='404')

@app.route('/transaction', methods=['POST'])
def create_transaction():
    req_data = request.get_json()
    schema = TransactionSchema()  

    try:     
        data = schema.load(req_data)
    except ValidationError as err:
        return jsonify(status='422', res='failure', error=err.messages)
    
    payer = db.get_user_by_id(data['payer_id'])
    payee = db.get_user_by_id(data['payee_id'])

    if not payer or not payee:
        return jsonify(error=f"Error! Payer with id '{data['payer_id']}' or payee with id '{data['payee_id']}' was not found!", status='404')

    if payer['balance'] < data['amount']:
        return jsonify(status='400', error=f"Insufficient balance for payer with id {data['payer_id']}")

    payer['balance']  -= data['amount']
    payee['balance']  += data['amount']    
    db.update_balance(payer['id'], payer['balance'])
    db.update_balance(payee['id'], payee['balance'])
    return jsonify(payer=payer, payee=payee, amount=data['amount'], status='200', msg='Success creating a new transaction!')

if __name__ == "__main__":
    initialize_db()
    app.run(debug=True)