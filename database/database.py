import os
from pymongo import MongoClient
from bson import ObjectId
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
    
    def c_pedido(self, rut, monto_total, lista_productos):
        try:
            #esta función se realiza con un update en vez de un insert para que el campo fecha_pedido sea creado de forma automática
            #a partir de la fecha actual del sistema donde esté la base de datos, esto usando el método $currentDate que solo está disponible en update
            #si se usara un datetime creado por el cliente, se podría insertar una fecha erronea al insertarse la del sistema del cliente
            nuevo_id = ObjectId() #genera un _id no existente en la base de datos
            cursor = db[COL_PEDIDOS].update_one(
                {
                    "_id": nuevo_id #usará este _id para buscar el pedido en la base de datos, el cual no existe en la base de datos
                    #usará upsert=True para insertar los datos especificados por $setOnInsert en caso de que la busqueda no exista en la bd
                    #además, usará este mismo _id para la inserción por ser el filtro de busqueda usado
                },
                {
                    "$setOnInsert": #indica lo que se insertará
                    {
                        "rut_cliente" : rut,
                        "monto_total": monto_total,
                        "productos": lista_productos #se crea el array vacío, será rellenado más tarde
                    },
                    "$currentDate": #actualiza el campo de fecha_pedido con la fecha actual del sistema
                    {
                        "fecha_pedido" : True
                    }
                },
                upsert=True
            )
            resultado = cursor.acknowledged
            if resultado:
                print("Se ingresó el pedido correctamente.")
            else:
                print("Hubo un error al ingresar el pedido.")
        except Exception as e:
            print(e)
    
    def r_productos_anadir_pedido(self): #usada para agregar productos al pedido
        try:
            cursor = db[COL_PRODUCTOS].find()
            resultado = list(cursor)
            if resultado:
                return resultado
            else:
                print("No se encuentran productos.")
                return False
        except Exception as e:
            print(e)
    
    def r_comp_rut(self, rut): #comprueba que el rut exista en la bd
        try:
            cursor = db[COL_CLIENTES].find({"rut":rut})
            resultado = list(cursor)
            if resultado:
                return True
            else:
                return False
        except Exception as e:
            print(e)