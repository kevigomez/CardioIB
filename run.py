from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    # Procesa los datos del formulario aquí
    return f"Gracias, {name}. Hemos recibido tu correo: {email}"

if __name__ == '__main__':
    app.run(debug=True)
