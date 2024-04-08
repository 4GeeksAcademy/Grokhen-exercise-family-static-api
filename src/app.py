"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_all_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200

@app.route('/member/<int:id>', methods=['GET'])
def get_member(id):
    member = jackson_family.get_member(id)
    if member is not None:
        return jsonify({
            "id":member["id"],
            "first_name":member["first_name"],
            "last_name":jackson_family.last_name,
            "age":member["age"],
            "lucky_numbers":member["lucky_numbers"]
        }), 200
    else:
        return "No se encontró ningún miembro con el ID proporcionado", 404

@app.route('/member', methods=['POST'])
def post_member():    
    body = request.get_json()
    if 'first_name' not in body or 'age' not in body or 'lucky_numbers' not in body:
        return jsonify({'error': 'Se requieren todos los campos: first_name, age, lucky_numbers'}), 400
    new_member = {
        'id': body['id'],
        'first_name': body['first_name'],
        'age': body['age'],
        'lucky_numbers': body['lucky_numbers']
    }
    jackson_family.add_member(new_member)

    return jsonify({"message": "Miembro agregado correctamente"}), 200

@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member(id):
    deleted = jackson_family.delete_member(id)
    if deleted:
        return jsonify({"done": True}), 200 
    else:
        return jsonify({"error": "Miembro no encontrado"}), 404  

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
