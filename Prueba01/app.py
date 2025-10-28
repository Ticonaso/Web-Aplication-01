from flask import Flask, jsonify, request, render_template
from flask_mysqldb import MySQL
from flask_cors import CORS
from config import config
 

app = Flask(__name__)
CORS(app)  # Habilitar CORS para la aplicación Flask
mysql = MySQL(app)  # Crear instancia de MySQL
conexion = mysql  # Usar la instancia como conexión

#Listar
@app.route('/productos', methods=['GET'])
def listar_cursos():
    try:
        cursor = conexion.connection.cursor()
        sql="SELECT id_producto, nombre, marca FROM productos"
        cursor.execute(sql)
        datos=cursor.fetchall()
        productos=[]
        for fila in datos:
            producto={
                'id_producto': fila[0],
                'nombre': fila[1],
                'marca': fila[2]
            }
            productos.append(producto)
        return jsonify({"productos": productos, "mensaje": "Producto listados"})     
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': "Error"})


#Cuando no se encuentra una pagina
def pagina_no_encontrada(error):
    return "<h1>La pagina no existe </h1>", 404

#Leer
@app.route('/productos/<codigo>', methods=['GET'])
def leer_cursos(codigo):
    try:
        cursor = conexion.connection.cursor()
        sql="SELECT id_producto, nombre, marca FROM productos WHERE id_producto = '{0}'".format(codigo)
        cursor.execute(sql)
        datos=cursor.fetchone()
        if datos != None:
            productos={
                'id_producto': datos[0],
                'nombre': datos[1],
                'marca': datos[2]
            }
            return productos
        else:
            return jsonify(
                {'mensaje': "Producto no encontrado", "exito": False})    
    except Exception as ex:
        return jsonify({'mensaje': "Error", "exito": False})

#registrar
@app.route('/productos/', methods=['POST'])
def registrar_producto():
    try:
        print(request.json)
        cursor = conexion.connection.cursor()
        sql = """INSERT INTO productos (id_producto, nombre, marca)
                 VALUES (%s, %s, %s)"""
        datos = (
            request.json['id_producto'],
            request.json['nombre'],
            request.json['marca']
        )
        cursor.execute(sql, datos)
        conexion.connection.commit()  # confirma la acción de inserción
        return jsonify({'mensaje': "Producto Registrado", "exito": True})
    
    except Exception as ex:
        print(f"Error: {ex}")
        return jsonify({'mensaje': "Error", "exito": False})

#Eliminar
@app.route('/productos/<codigo>', methods=['DELETE'])
def eliminar_cursos(codigo):
    try:
        cursor = conexion.connection.cursor()
        sql="DELETE FROM productos WHERE id_producto = '{0}'".format(codigo)
        cursor.execute(sql)
        conexion.connection.commit() #confirma la accion de eliminacion
        return jsonify({'mensaje': "Producto Eliminado", "exito": True})    
    except Exception as ex:
        return jsonify({'mensaje': "Error", "exito": False})    

#Actualizar
@app.route('/productos/<codigo>', methods=['PUT'])
def actualizar_cursos(codigo):
    try:
        cursor = conexion.connection.cursor()
        sql = "UPDATE productos SET nombre = %s, marca = %s WHERE id_producto = %s"
        cursor.execute(sql, (request.json['nombre'], request.json['marca'], codigo))
        conexion.connection.commit() #confirma la accion de actualizacion
        return jsonify({'mensaje': "Producto Actualizado", "exito": True})    
    except Exception as ex:
        return jsonify({'mensaje': "Error", "exito": False})


@app.route('/')
def index():
    return render_template('index.html')

#Main
if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()
    

