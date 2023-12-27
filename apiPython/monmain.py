from flask import Flask, request

app = Flask(__name__)

robot_host = 'telo-robot.loal'  # Valeur initiale du robotHost

@app.route('/api/robot-host', methods=['GET'])
def get_robot_host():
    return {'robotHost': robot_host}

@app.route('/api/robot-host', methods=['POST'])
def set_robot_host():
    data = request.json
    new_robot_host = data.get('robotHost')
    global robot_host
    robot_host = new_robot_host
    return 'RobotHost mis à jour avec succès'

@app.route('/api/program', methods=['GET'])
def get_program():
    with open('../../../Downloads/projetJoystick/host.py', 'r') as file:
        program_code = file.read()
    return {'programCode': program_code}

if __name__ == '__main__':
    app.run()