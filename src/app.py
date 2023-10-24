"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

jackson_family = FamilyStructure("Jackson")

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_members():
    members = jackson_family.get_all_members()
    
    return jsonify(members), 200

@app.route('/member', methods=['POST'])
def add_member():
    if not request.is_json:
        return jsonify({"msg": "La solicitud debe ser de tipo JSON"}), 400
    new_member = request.json
    if "first_name" not in new_member or "age" not in new_member:
        return jsonify({"msg": "Campos 'first_name' y 'age' son obligatorios"}), 400
    jackson_family.add_member(new_member)
    return jsonify({"msg": "Miembro creado"}), 200

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_family_member(member_id):
    eliminar_familiar = jackson_family.delete_member(member_id)
    if eliminar_familiar:
        return jsonify({"done": True}), 200
    return jsonify({"msg":"Familiar no encontrado"}), 400

@app.route('/member/<int:member_id>', methods=['PUT'])
def update_family_member(member_id):
    new_member = request.json
    actualizar_family_member = jackson_family.update_member(member_id, new_member)
    if not actualizar_family_member:
        return jsonify({"msg": "miembro no encontrado"}), 400
    return jsonify({"msg":"Familiar actualizado"}), 200

@app.route('/member/<int:member_id>', methods=['GET'])
def get_one_member(member_id):
    familiar_encontrado = jackson_family.get_member(member_id)
    if not familiar_encontrado:
        return jsonify({"msg": "Familiar no encontrado"}), 200
    return jsonify(familiar_encontrado), 200

    





if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
