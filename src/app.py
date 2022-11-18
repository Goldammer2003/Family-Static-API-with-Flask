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

@app.route('/members', methods=['GET']) #gettingAllFamilyMembers
def getAllFamilyMembers():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
   


    return jsonify(members), 200


@app.route('/member/<int:id>', methods =['GET'])
 #/gettingFamilyMember/<int:member_id>
def getOneMember(id):
    member=jackson_family.get_member(id) 
    if member is None:
        raise APIException ('this member does not exist',400)
    response_body = {
       
        "member": member
    }


    return jsonify(response_body), 200

@app.route ("/member", methods = ['POST']) #/addingFamilyMember
def addFamilyMember (): 
    requestbody=request.get_json (force=True) #Access body of request, request looks like {"key":"value"}
    # access value of objects like this: objectname ["keyname"]
    jackson_family.add_member({"id":jackson_family._generateId(), "first_name":requestbody["first_name"], "age":requestbody["age"],"lucky_numbers":requestbody["lucky_numbers"]})
    return jsonify ("member added"),200
# this only runs if `$ python src/app.py` is executed
@app.route('/member/<int:id>', methods =['DELETE'])
def deletingFamilymember (id):
    jackson_family.delete_member(id)
    return jsonify ({"done":True}),200


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)

