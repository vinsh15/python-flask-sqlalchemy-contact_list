"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Contact
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/contacts', methods=['GET'])
def handle_contact():
    contacts = Contact.query.all()
    response_body=[]
    for contact in contacts:
        response_body.append(contact.serialize())

    return jsonify(response_body), 200


@app.route('/contacts', methods=['POST'])
def add_new_contact():
    body = request.get_json()
    if isinstance (body, dict):
        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        if 'full_name' not in body:
            raise APIException('You need to specify the username', status_code=400)
        if 'email' not in body:
            raise APIException('You need to specify the email', status_code=400)
        if 'address' not in body:
            raise APIException('You need to specify the address', status_code=400)
        if 'phone' not in body:
            raise APIException('You need to specify the phone', status_code=400)
    else: return "no es un diccionario"

    # at this point, all data has been validated, we can proceed to inster into the bd
    contact1 = Contact(full_name=body['full_name'], email=body['email'], address=body['address'], phone=body['phone'])
    db.session.add(contact1)
    db.session.commit()
    return "ok", 200

@app.route('/contacts/<int:position>', methods=['PATCH'])
def upgrade_contact(position):
    body = request.json()
    contact_to_upgrade = Contact.query.get(position)
    if 'full_name' is in body
        new_full_name = body['full_name']
        contact_to_upgrade.full_name = new_full_name
    if 'email' is in body
        new_email = body['email']
        contact_to_upgrade.email = new_email
    if 'address' is in body
        new_address = body['address']
        contact_to_upgrade.address = new_address
    if 'phone' is in body
        new_phone = body['phone']
        contact_to_upgrade.phone = new_phone

    db.session.commit()



@app.route('/contacts/<int:position>', methods=['GET'])
def handle_one_contact(position):
    contact = Contact.query.get(position)
    if contact is None:
        return "NO EXISTE", 404
    else:
        return jsonify(contact.serialize()), 202

@app.route('/contacts/<int:position>', methods=['DELETE'])
def delete_contact(position): 
    db.session.delete(Contact.query.get_or_404(position) )
    db.session.commit() 
    return '', 204

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
