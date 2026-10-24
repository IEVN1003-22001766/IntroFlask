from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS

from config import config

app = Flask(__name__)
CORS(app)

app.config.from_object(config['development'])
con=MySQL(app)

def fila_a_diccionario(cursor, fila):
    columnas= [columna[0] for columna in cursor.description]
    return dict(zip(columnas,fila))

@app.route("/alumnos", methods=['GET'])
def lista_alumnos():
    try:
        cursor = con.connection.cursor()
        sql="select * from alumnos"
        cursor.execute(sql)
        datos = cursor.fetchall()
        alumnos=[]

        for fila in datos:
            alumno={"matricula":fila[0], "nombre":fila[1],
                    "apaterno":fila[2], "amaterno":fila[3],
                    "correo":fila[4]}
            alumnos.append(alumno)

        return jsonify({'alumnos':alumnos,'mensaje':"Lista de Alumnos",'exito':True})
    except Exception as ex:
        return jsonify({"mensage": "error{}".format(ex), 'exito':False})

@app.route("/alumnos/<string:matricula>",methods=['GET'])
def leer_alumno_bd(matricula):
    cursor=None
    try:
        cursor=con.connection.cursor()
        cursor.execute("""SELECT * FROM alumnos
        WHERE matricula=%s""",(matricula,))
        fila=cursor.fetchone()
        if fila is None:
            return jsonify({
                'mensaje': 'Alumno no encontrado',
                'exito': False
            }),404
        alumno=fila_a_diccionario(cursor,fila)
        return jsonify({
            'alumno': alumno,
            'exito': True
        }),200
    except Exception as ex:
        return jsonify({
            'mensaje': "ERROR AL CONSULTAR EL ALUMNO",
            'exito': False
        }), 500
    finally:
        if cursor is not None:
            cursor.close()

@app.route("/alumnos",methods=['POST'])
def registrar_alumno():
    datos.request.get_json(silent=True)
    if not isinstance(datos,dict):
        return jsonify({
            'mensaje': 'Se requiere un objeto JSON',
            'exito': False
        }),400
    campos=[
        'matricula', 'nombre', 'apaterno', 'amaterno', 'correo'
    ]
    if any(
        campo not in datos
        or not isinstance(datos[campo],str)
        or not datos[campo].strip()
        for campo in campos
    ):
        return jsonify({
            'mensaje': 'FALTAN CAMPOS OBLIGATORIOS'
            'exito': False
        }),400
    cursor=None
    try:
        cursor.execute("""INSERT INTO alumnos (matriucla, nombre, apaterno, amaterno, correo) VALUES (%s, %s, %s, %s, %s)""", tuple(datos[campo].strip() for campo in campos))

        con.connection.commit()

        return jsonify({
            'mensaje': 'Alumno regstrado correctamente',
            'exito': True
        }), 201

    except Exception as ex:
        con.connection.rollback()

        return jsonify({
            'mensaje': 'Error al registrar al alumno: {}'.format(ex)
            'exito': False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()

def pagina_no_encontrada(error):
    return "<h1>Pagina no encontrada</h1>"

if __name__ == '__main__':
    app.register_error_handler(404,pagina_no_encontrada)
    app.run(host='0.0.0.0', port=5000)