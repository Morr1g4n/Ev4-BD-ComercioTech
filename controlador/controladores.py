from database.database import MongoManager
from readchar import readkey
from datetime import datetime, timedelta
from vista.prints import PrintsBD
import re
import subprocess

dbprint = PrintsBD()
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
    
    def create_pedido(self):
        print("(Pulse enter vacío para cancelar la operación)")
        productos_anadir = [] #usado para mostrar el resumen de los productos y añadirlos al pedido
        monto_total = 0 #usado para modificar el monto total del pedido al final del calculo
        while True:
            try:
                regex_rut = re.compile("^\\d{8}-\\d$")
                rut = input("Ingrese RUT del cliente (sin puntos y con guión): ")
                rut = rut.strip()
                comprobacion = manager.r_comp_rut(rut)
                if not rut:
                    return False
                elif not regex_rut.match(rut):
                    raise ValueError
                elif not comprobacion:
                    print("El RUT ingresado no existe.")
                else:
                    break
            except ValueError:
                print("Ingrese un RUT válido")
        print("Ahora ingresará los productos al pedido")
        self.continuar()
        lista_productos = manager.r_productos_anadir_pedido()
        if not lista_productos:
            self.continuar()
            return False
        for indice, producto in enumerate(lista_productos, start=1):
            producto["numero_producto"] = indice
        
        seguir = True
        while seguir:
            dbprint.print_productos_disponibles(lista_productos)
            try:
                seleccion = int(input("Seleccione un producto: "))
                producto_elegido = next((p for p in lista_productos if p["numero_producto"] == seleccion), None)
                #usa el generador para recorrer toda la lista de productos filtrando con if si es que el número del producto corresponde a la selección
                #next pide al generador el primer elemento (producto) que coinicida con la condición if y detiene el generador cuando se cumple
                #en caso de que no haya ninguna coincidencia, el generador entrega None y pide realizar la seleccion otra vez
                if producto_elegido:
                    while True:
                        try:
                            cantidad = int(input("Ingrese cantidad del producto: "))
                            if cantidad >= 1:
                                precio_unitario = int(producto_elegido.get("precio"))
                                precio_total = cantidad * precio_unitario
                                monto_total += precio_total
                                break
                            else:
                                print("La cantidad no puede ser menor a 1")
                        except ValueError:
                            print("Ingrese un valor válido")
                    producto_final = {
                        "producto_id" : producto_elegido.get("_id"),
                        "nombre" : producto_elegido.get("nombre"),
                        "cantidad" : cantidad,
                        "precio" : precio_total
                    }
                    productos_anadir.append(producto_final)
                else:
                    print("Seleccione un producto válido")
                    self.continuar()
                    continue #evita que se pregunte si se quiere añadir otro producto, evitando ingresar un pedido vacío al continuar con el loop saltandose las siguientes líneas
            except ValueError:
                print("Ingrese un valor válido")
                self.continuar()
                continue
            while True:
                otro = input("¿Quiere añadir otro producto?(S/N): ")
                otro = otro.strip().lower()
                if otro == "s":
                    seguir = True
                    break
                elif otro == "n":
                    seguir = False
                    break
                else:
                    print("Seleccione una opción válida")

        if not productos_anadir: #si la lista de productos está vacía, se evita que se siga creando el pedido (no debería ser posible pero sirve como otra barrera de seguridad)
            print("El pedido no puede estar vacío, cancelando..")
            self.continuar()
            return False
        dbprint.print_resumen_crear_pedido(productos_anadir, monto_total, rut)
        while True:
            eleccion = input("¿Desea crear el pedido?(S/N): ")
            eleccion = eleccion.strip().lower()
            if eleccion == "s":
                for producto in productos_anadir: #elimina el nombre del producto antes de insertarlo, solo fue usado para visualización
                    del producto["nombre"]
                manager.c_pedido(rut, monto_total, productos_anadir)
                self.continuar()
                self.limpiarconsola()
                return True
            elif eleccion == "n":
                return False
            else:
                print("Seleccione una opción válida")
                

