from database.database import MongoManager
from readchar import readkey
from pymongo.errors import ConnectionFailure
import subprocess

manager = MongoManager()

class Menu():
    def limpiarconsola(self):
        subprocess.run("cls||clear", shell=True)

    def continuar(self):
        print("Presione cualquier tecla para continuar...")
        readkey()
        self.limpiarconsola()
    
    def menuInicial(self):
        self.limpiarconsola()
        while True:
            print("-" * 5 + "Gestor Admin ComercioTech" + "-" * 5)
            print("1.- Gestión Clientes")
            print("2.- Gestión Pedidos")
            print("3.- Gestión Productos")
            print("0.- Salir")
            eleccion = input("Elija una opción: ")
            if eleccion == "1":
                self.menuClientes()
            elif eleccion == "2":
                self.menuPedidos()
            elif eleccion == "3":
                self.menuProductos()
            elif eleccion == "0":
                print("Adiós!")
                raise SystemExit
            else:
                self.limpiarconsola()
                print("Seleccione una opción válida")
        
    def menuClientes(self):
        self.limpiarconsola()
        while True:
            print("-" * 5 + "Gestor Clientes" + "-" * 5)
            print("1.- Crear cliente")
            print("2.- Ver clientes")
            print("3.- Actuaizar datos cliente")
            print("4.- Eliminar cliente")
            print("0.- Volver atrás")
            eleccion = input("Elija una opción: ")
            if eleccion == "1":
                pass
            elif eleccion == "2":
                self.limpiarconsola()
                manager.r_clientes_todos()
                self.continuar()
            elif eleccion == "3":
                pass
            elif eleccion == "4":
                pass
            elif eleccion == "0":
                self.menuInicial()
            else:
                self.limpiarconsola()
                print("Seleccione una opción válida")
    
    def menuPedidos(self):
        self.limpiarconsola()
    
    def menuProductos(self):
        self.limpiarconsola()
