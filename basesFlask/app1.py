from flask import Flask, render_template, request
import math

app = Flask(__name__)

@app.route("/") #Decorador o ruta
def index():
    titulo='Pagina de Inicio'
    listado = ['Python', 'Flask', 'Jinja2', 'HTML', 'CSS']
    return render_template("index.html", titulo=titulo, listado=listado)

@app.route("/operasbas", methods=['GET','POST'])
def operasbas():
    n1=0
    n2=0
    res=0
    operacion=''

    if request.method == 'POST':
        n1 = request.form.get('n1')
        n2 = request.form.get('n2')
        if request.form.get('operacion') == 'sumar':
            res = float(n1) + float(n2)
        elif request.form.get('operacion') == 'restar':
            res = float(n1) - float(n2)
        elif request.form.get('operacion') == 'multiplicar':
            res = float(n1) * float(n2)

        
    return render_template('operasbas.html', n1=n1, n2=n2, res=res)

@app.route('/distancia', methods=['GET','POST'])
def distancia():
    x1 = 0
    y1 = 0
    x2 = 0
    y2 = 0
    res = 0

    if request.method == 'POST':
        x1 = float(request.form.get('x1') or 0)
        y1 = float(request.form.get('y1') or 0)
        x2 = float(request.form.get('x2') or 0)
        y2 = float(request.form.get('y2') or 0)
        
        res = (x2 - x1)**2 + (y2 - y1)**2
        res = math.sqrt(res)

    return render_template('distancia.html', x1=x1, y1=y1, x2=x2, y2=y2, res=res)

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