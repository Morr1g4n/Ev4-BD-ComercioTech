import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pymongo.database import Database
from pymongo.errors import ConnectionFailure
from datetime import datetime, timedelta
from vista.prints import PrintsBD
from dotenv import load_dotenv

load_dotenv()
uri = os.getenv("MONGO_URI")
DB_NAME = "carrito_compras"
COL_CLIENTES = "clientes"
COL_PEDIDOS = "pedidos"
COL_PRODUCTOS = "productos"

def conexion_mongo(uri = uri, nombre_bd = DB_NAME) -> Database:
        try:
            cliente = MongoClient(uri, serverSelectionTimeoutMS = 3000, server_api=ServerApi(version="1", strict=True, deprecation_errors=True))
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