import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pymongo.database import Database
from pymongo.errors import ConnectionFailure
from datetime import datetime, timedelta
from vista.prints import PrintsBD
from dotenv import load_dotenv

uri =  "mongodb://127.0.0.1:27017"
DB_NAME = "gestor_comerciotech"
COL_CLIENTES = "clientes"
COL_PEDIDOS = "pedidos"
COL_PRODUCTOS = "productos"

def conexion_mongo(uri = uri, nombre_bd = DB_NAME) -> Database:
        try:
            cliente = MongoClient(uri, serverSelectionTimeoutMS = 3000)
            cliente.admin.command("ping")
            db = cliente[nombre_bd]
            return db
        except ConnectionFailure as error:
            raise RuntimeError(f"No fue posible la conexión: {error}")

db = conexion_mongo()
dbprint = PrintsBD()

#las funciones empezarán con c(create), r(read), u(update), d(delete) dependiendo de su funcionalidad, servirá como nomenclatura, incluir la colección que va a afectar
#agregar prints en módulo prints dentro de vista
class MongoManager:
    def r_clientes_todos(self):
        try:
            cursor = db[COL_CLIENTES].find()
            resultados = list(cursor)
            if resultados:
                dbprint.print_clientes(resultados)
            else:
                print("No se encuentran resultados")
        except Exception as e:
             print(e)
    
    def c_cliente(self, data):
        try:
            cursor = db[COL_CLIENTES].insert_one(
                {
                    "rut" : data.get("rut"),
                    "nombre" : data.get("nombre"),
                    "fecha_registro" : data.get("fecha_registro"),
                    "direccion" : data.get("direccion"),
                    "telefono" : data.get("telefono"),
                    "email" : data.get("email")
                }
            )
            resultado = cursor.acknowledged 
            #la función de insert_one retorna una instancia de InsertOneResult (se puede imprimir cursor para ver el objeto que genera)
            #se puede usar el atributo acknowledged para saber si se insertó o no (booleano)
            if resultado:
                print("Se insertó correctamente el cliente.")
            else:
                print("Hubo un problema al insertar el cliente.")
        except Exception as e:
            print(e)