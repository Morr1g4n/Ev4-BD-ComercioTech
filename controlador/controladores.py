from database.database import MongoManager
from readchar import readkey
from datetime import datetime, timedelta
import re
import subprocess

manager = MongoManager()

class Controladores:
    def limpiarconsola(self):
        subprocess.run("cls||clear", shell=True)

    def continuar(self):
        print("Presione cualquier tecla para continuar...")
        readkey()
        self.limpiarconsola()

    def read_clientes_todos(self):
        self.limpiarconsola()
        manager.r_clientes_todos()
        self.continuar()

    def create_cliente(self):
        print("(Pulse enter vacío para cancelar la operación)")
        while True:
            try:
                regex_rut = re.compile("^\\d{8}-\\d$")
                rut = input("Ingrese RUT (sin puntos y con guión): ")
                rut = rut.strip()
                if not rut:
                    return False #se usará en caso de querer cancelar toda la operación, volverá al menú
                elif not regex_rut.match(rut):
                    raise ValueError
                else:
                    break
            except ValueError:
                print("Ingrese un RUT válido")
        
        pnombre = input("Ingrese primer nombre: ")
        if not pnombre:
            return False
        pnombre = pnombre.strip().capitalize()
        apellido = input("Ingrese primer apellido: ")
        if not apellido:
            return False
        apellido = apellido.strip().capitalize()
        nombre = pnombre + " " + apellido
        
        while True:
            try:
                fecha_registro = input("Ingrese fecha de registro(Formato AAAA-MM-DD, incluya guión): ")
                if fecha_registro == "":
                    return False
                fecha_registro = fecha_registro.strip()
                fecha_registro = datetime.strptime(fecha_registro, "%Y-%m-%d") #lanza value error si el formato es incorrecto o la fecha es inválida, no hace falta un raise
                break
            except ValueError:
                print("Ingrese una fecha válida")

        direccion = input("Ingrese dirección: ")
        direccion = direccion.strip()
        if not direccion:
            return False
        
        while True:
            try:
                regex_tel = re.compile("^\\+569\\d{8}$")
                telefono = input("Ingrese telefono: +569")
                telefono = telefono.strip()
                if not telefono:
                    return False
                telefono = "+569" + telefono
                if not regex_tel.match(telefono):
                    raise ValueError
                else:
                    break
            except ValueError:
                print("Ingrese un teléfono válido")
        
        email = input("Ingrese e-mail: ")
        if not email:
            return False
        email = email.strip().lower()

        cliente = {
            "rut": rut,
            "nombre": nombre,
            "fecha_registro": fecha_registro,
            "direccion": direccion,
            "telefono": telefono,
            "email": email
        }

        print("Datos cliente a añadir:")
        print(f"RUT: {cliente["rut"]} | Nombre: {cliente["nombre"]} | Fecha Registro: {cliente["fecha_registro"]} | Dirección: {cliente["direccion"]} | Teléfono: {cliente["telefono"]} | E-mail: {cliente["email"]}")
        while True:
            eleccion = input("¿Quiere agregar a este cliente? (S/N): ")
            eleccion = eleccion.strip().lower()
            if eleccion == "s":
                manager.c_cliente(cliente)
                self.continuar()
                return True #solo usarlo al final, evita que aparezca operación cancelada por el if en menu
            elif eleccion == "n":
                return False