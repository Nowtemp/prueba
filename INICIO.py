from flask import Flask,jsonify,json,render_template,request,redirect
from classconnect import *
import pymysql

app = Flask(__name__)

@app.route("/")
def presentation():
    return "Bienvenido a mi pagina web."

@app.route("/<name>")
def greeting(name):
    return "Hola "+str(name)

@app.route("/add", methods=["POST"])
def add():
    try:
        nombre=request.form.get("nombre")
        apellido=request.form.get("apellido")
        conectar=Classconnect()
        conectar.EjecutarSQL("INSERT INTO employees (Nombre,Apellido) VALUES('"+nombre+"','"+apellido+"')")
        datos=conectar.DevolverDatos()
        conectar.RealizarCambio()
        print (datos)
    except Exception:
        conectar.DeshacerCambio()
        print ("¡ERROR! ¡No se ha podido realizar el alta!")
    return redirect("/all")

@app.route("/update", methods=["POST"])
def update():
    id=request.form.get("id")
    nombre=request.form.get("nombre")
    apellido=request.form.get("apellido")
    conectar=Classconnect()
    conectar.EjecutarSQL("UPDATE employees SET Nombre='"+nombre+"',Apellido='"+apellido+"' WHERE id="+id)
    conectar.RealizarCambio()
    return redirect("/all")

@app.route("/delete", methods=["GET","POST"])
def delete():
    try:
        id=request.form.get('id')
        conectar=Classconnect()
        conectar.EjecutarSQL("DELETE FROM employees WHERE id="+id)
        conectar.RealizarCambio()
    except Exception:
        conectar.DeshacerCambio()
        print ("¡ERROR! ¡No se ha podido borrar el registro!")
    return redirect("/all")

@app.route("/list")
def listadoalumno():
    conectar=Classconnect()
    conectar.EjecutarSQL("SELECT * FROM employees")
    datos=conectar.DevolverDatos()
    respuesta=jsonify(datos)
    conectar.CerrarBase()
    return respuesta

@app.route("/all")
def listadoall():
    conectar=Classconnect()
    conectar.EjecutarSQL("SELECT * FROM employees")
    data=conectar.DevolverDatos()
    conectar.CerrarBase()
    return render_template("index.html", datos=data)

if __name__ == "__main__":
    app.run()