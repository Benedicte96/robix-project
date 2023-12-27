from flask import jsonify, request, Flask
#from flask_cors import CORS
import api 


app = Flask(__name__)
app.config["DEBUG"] = True
#CORS(app)

all_heroes = [{'id': 11, 'name': 'Dr Nice'},
    {'id': 11, 'name': 'Dr Nice'},
    {'id': 11, 'name': 'Dr Nice'},
    {'id': 11, 'name': 'Dr Nice'},
    {'id': 11, 'name': 'Dr Nice'},
    {'id': 11, 'name': 'Dr Nice'},
    {'id': 11, 'name': 'Dr Nice'}]

@app.route('/heroes', methods=['GET'])
def heroes():
    return jsonify(all_heroes)

@app.route('/detail/<id>', methods =['GET'])
def detail(id):


    for x in all_heroes:
        if x['id'] == id:
            return jsonify(x)



app.run()

