from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

import subprocess
import asyncio
import os
app = Flask(__name__)
CORS(app)

# Valeur initiale du robotHost
robot_host = 'telo-robot.local'
param = 'cmd_vel'

@app.route('/api/run-joystick', methods=['POST'])
async def run_joystick():
#     print("Route /api/run-joystick appelée.")
#     asyncio.create_task(run_joystick_background())
#     return jsonify({'message': 'Script en cours d execution en arriere-plan'})


# async def run_joystick_background():
#     print("Exécution du script Python en arrière-plan.")
#     await asyncio.sleep(0)

    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(current_dir, 'host.py')
        subprocess.Popen(['python', script_path])
    except Exception as e:
        print("erreur lors de l'exécution")



@app.route('/api/robot-host', methods=['GET'])
def get_robot_host():
    return jsonify({'robotHost': robot_host,'param': param})

@app.route('/api/robot-host', methods=['POST'])
def set_robot_host():
    data = request.json
    value = data['value']
    value_ = data['value_']

    global robot_host
    global param
    robot_host = value# Récupère la valeur envoyée par la requête POST
    param = value_

    # Effectuez les opérations souhaitées avec la valeur reçue
    # Par exemple, renvoyez une réponse contenant la valeur
    #response = {'message': 'Valeur reçue avec succès', 'value': value, value_}
    response = {'message': 'Valeurs reçues avec succès', 'value': value, 'value2': value_}

    return jsonify(response)


@app.route('/api/stop-joystick', methods=['POST'])
def stop_joystick():
    try:
        # Mettez ici le code pour arrêter le script en arrière-plan.
        # Vous pouvez utiliser les méthodes ou techniques appropriées pour arrêter le script.
        # Par exemple, vous pouvez envoyer un signal d'arrêt au processus ou utiliser une variable pour contrôler la boucle while dans le script.

        # Exemple : utilisez une variable pour arrêter la boucle dans le script
        global running
        running = False

        return jsonify({'message': 'Script arrêté avec succès'})

    except Exception as e:
        return jsonify({'message': 'Erreur lors de l\'arrêt du script', 'error': str(e)})



@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route('/api/program', methods=['GET'])
def get_program():
    with open('../../Downloads/projetJoystick/host.py', 'r') as file:
        program_code = file.read()
    return jsonify({'programCode': program_code})


if __name__ == '__main__':
    app.run()
