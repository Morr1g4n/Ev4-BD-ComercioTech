from tabulate import tabulate
from datetime import datetime, timedelta

#reusar prints cuando sea posible, solo crear nuevos cuando sea necesario para algo más especifico (mostrar diferentes campos)
class PrintsBD:
    def print_clientes(self, lista):
        tabla = []
        headers = ["RUT", "Nombre", "Fecha Registro", "Dirección", "Teléfono", "E-mail"]
        for resultado in lista:
            rut = str(resultado.get("rut", "N/A")) #usar .get en vez de [] permite manejar de mejor manera los datos en caso de que la clave no exista
            #evita erores de KeyError
            nombre = str(resultado.get("nombre", "N/A"))
            #Validación en caso de que la fecha esté como objeto date o como string en formato ISO, por seguridad
            fecha_registro_cruda = resultado.get("fecha_registro") #obtiene fecha cruda de la bd
            if isinstance(fecha_registro_cruda, datetime):
                fecha_registro = fecha_registro_cruda.strftime("%Y-%m-%d")
            elif fecha_registro_cruda: #en caso que sea otro tipo
                try:
                    fecha_registro = datetime.strftime(datetime.fromisoformat(str(fecha_registro_cruda)), "%Y-%m-%d") #lanza ValueError si no corresponde a una string ISOFORMAT y lo saca por string en el except
                except ValueError:
                    fecha_registro = str(fecha_registro_cruda)
            else:
                fecha_registro = ("N/A") #en caso de que no exista
            direccion = str(resultado["direccion"])
            telefono = str(resultado["telefono"])
            email = str(resultado["email"])
            dato = [rut, nombre, fecha_registro, direccion, telefono, email]
            tabla.append(dato)
        print("Clientes encontrados")
        print(tabulate(tabla, headers=headers, tablefmt="simple_grid"))
    
    def print_productos_disponibles(self, lista):
        tabla = []
        headers = ["Número Producto", "Nombre", "Precio"]
        for producto in lista:
            numero_producto = str(producto.get("numero_producto"))
            nombre = str(producto.get("nombre"))
            precio = str(producto.get("precio"))
            dato = [numero_producto, nombre, precio]
            tabla.append(dato)
        print("Lista de productos")
        print(tabulate(tabla, headers=headers, tablefmt="simple_grid"))
    
    def print_productos_crear_pedido(self, lista):
        tabla = []
        headers = ["Producto", "Cantidad", "Precio Total"]
        for producto in lista:
            nombre = str(producto.get("nombre"))
            cantidad = str(producto.get("cantidad"))
            precio = str(producto.get("precio"))
            dato = [nombre, cantidad, precio]
            tabla.append(dato)
        print("Productos a añadir")
        print(tabulate(tabla, headers=headers, tablefmt="simple_grid"))