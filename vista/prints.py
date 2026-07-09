from tabulate import tabulate
from datetime import datetime, timedelta


# reusar prints cuando sea posible, solo crear nuevos cuando sea necesario para algo más especifico (mostrar diferentes campos)
class PrintsBD:
    def print_clientes(self, lista, title=True):
        tabla = []
        headers = ["RUT", "Nombre", "Fecha Registro", "Dirección", "Teléfono", "E-mail"]
        for resultado in lista:
            rut = str(
                resultado.get("rut", "N/A")
            )  # usar .get en vez de [] permite manejar de mejor manera los datos en caso de que la clave no exista
            # evita erores de KeyError
            nombre = str(resultado.get("nombre", "N/A"))
            # Validación en caso de que la fecha esté como objeto date o como string en formato ISO, por seguridad
            fecha_registro_cruda = resultado.get(
                "fecha_registro"
            )  # obtiene fecha cruda de la bd
            if isinstance(fecha_registro_cruda, datetime):
                fecha_registro = fecha_registro_cruda.strftime("%Y-%m-%d")
            elif fecha_registro_cruda:  # en caso que sea otro tipo
                try:
                    fecha_registro = datetime.strftime(
                        datetime.fromisoformat(str(fecha_registro_cruda)), "%Y-%m-%d"
                    )  # lanza ValueError si no corresponde a una string ISOFORMAT y lo saca por string en el except
                except ValueError:
                    fecha_registro = str(fecha_registro_cruda)
            else:
                fecha_registro = "N/A"  # en caso de que no exista
            direccion = str(resultado["direccion"])
            telefono = str(resultado["telefono"])
            email = str(resultado["email"])
            dato = [rut, nombre, fecha_registro, direccion, telefono, email]
            tabla.append(dato)

        if title:
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

    def print_resumen_crear_pedido(self, lista_prod, monto_total, rut):
        tabla = []
        tabla2 = [["Monto Total", monto_total], ["RUT Cliente", rut]]
        headers = ["Producto", "Cantidad", "Precio"]
        for producto in lista_prod:
            nombre = str(producto.get("nombre"))
            cantidad = str(producto.get("cantidad"))
            precio = str(producto.get("precio"))
            dato = [nombre, cantidad, precio]
            tabla.append(dato)
        print("Productos a añadir")
        print(tabulate(tabla, headers=headers, tablefmt="simple_grid"))
        print(tabulate(tabla2, tablefmt="simple_grid"))

    def print_pedidos(self, lista):
        # tabulate tiene una forma integrada de añadir indices, pero por la forma en que se debe mostrar la información acá, se añade de forma manual
        print("-" * 50)
        for indice, pedido in enumerate(lista, start=1):
            pedido["numero_pedido"] = indice

        for pedido in lista:
            lista_productos = pedido.get("productos")
            tabla = []
            headers = ["Nº Pedido", "RUT", "Fecha Pedido", "Monto Total"]
            numero_pedido = str(pedido.get("numero_pedido"))
            rut = str(pedido.get("rut_cliente"))
            fecha_pedido_cruda = pedido.get("fecha_pedido")
            if isinstance(fecha_pedido_cruda, datetime):
                fecha_pedido = fecha_pedido_cruda.strftime("%Y-%m-%d")
            elif fecha_pedido_cruda:
                try:
                    fecha_pedido = datetime.strftime(
                        datetime.fromisoformat(str(fecha_pedido_cruda)), "%Y-%m-%d"
                    )
                except ValueError:
                    fecha_pedido = str(fecha_pedido_cruda)
            else:
                fecha_pedido = "N/A"
            monto_total = str(pedido.get("monto_total"))
            dato = [numero_pedido, rut, fecha_pedido, monto_total]
            tabla.append(dato)
            print(tabulate(tabla, headers=headers, tablefmt="simple_grid"))
            print("Productos del pedido")
            tabla_prod = []
            headers_prod = ["Nombre", "Cantidad", "Precio"]
            for producto in lista_productos:
                nombre = str(producto.get("nombre"))
                cantidad = str(producto.get("cantidad"))
                precio = str(producto.get("precio"))
                dato_prod = [nombre, cantidad, precio]
                tabla_prod.append(dato_prod)
            print(tabulate(tabla_prod, headers=headers_prod, tablefmt="simple_grid"))
            print("-" * 50)
