from flask import Flask, render_template, render_templates

app = Flask(__name__)

@app.route('/GET')
def home():
    # Votre code ici pour générer le résultat
  return render_template('templates/index.html')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
