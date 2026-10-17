from flask import Flask, render_template

app = Flask(__name__)

@app.route("/") #Decorador o ruta
def index():
    titulo='Pagina de Inicio'
    listado = ['Python', 'Flask', 'Jinja2', 'HTML', 'CSS']
    return render_template("index.html", titulo=titulo, listado=listado)

@app.route("/hola")
def hola():
    return "<h1>Hola Esteban y a PWA</h1>"

@app.route("/user/<string:nom>")
def user(nom):
    return "<h1>Hola Usuario: {} </h1>".format(nom)

@app.route("/user/<int:id>/<string:username>")
def cuenta(id, username):
    return "ID: {} Nombre: {}".format(id,username)

@app.route("/suma/<float:n1>/<float:n2>")
def funcion(n1,n2):
    return "la suma es de: {}".format(n1+n2)

if __name__ == "__main__":
    app.run(debug=True)