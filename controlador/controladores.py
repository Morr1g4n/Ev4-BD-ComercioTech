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

    def read_pedidos_todos(self):
        self.limpiarconsola()
        manager.r_pedidos_todos()
        self.continuar()

    def read_productos_todos(self):
        self.limpiarconsola()
        manager.r_productos_all()
        self.continuar()

    def create_cliente(self):
        print("(Pulse enter vacío para cancelar la operación)")
        while True:
            try:
                regex_rut = re.compile("^\\d{8}-\\d$")
                rut = input("Ingrese RUT (sin puntos y con guión): ")
                rut = rut.strip()
                if not rut:
                    return False  # se usará en caso de querer cancelar toda la operación, volverá al menú
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
                fecha_registro = input(
                    "Ingrese fecha de registro(Formato AAAA-MM-DD, incluya guión): "
                )
                if fecha_registro == "":
                    return False
                fecha_registro = fecha_registro.strip()
                fecha_registro = datetime.strptime(
                    fecha_registro, "%Y-%m-%d"
                )  # lanza value error si el formato es incorrecto o la fecha es inválida, no hace falta un raise
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
            "email": email,
        }

        print("Datos cliente a añadir:")
        print(
            f"RUT: {cliente["rut"]} | Nombre: {cliente["nombre"]} | Fecha Registro: {cliente["fecha_registro"]} | Dirección: {cliente["direccion"]} | Teléfono: {cliente["telefono"]} | E-mail: {cliente["email"]}"
        )
        while True:
            eleccion = input("¿Quiere agregar a este cliente? (S/N): ")
            eleccion = eleccion.strip().lower()
            if eleccion == "s":
                manager.c_cliente(cliente)
                self.continuar()
                return True  # solo usarlo al final, evita que aparezca operación cancelada por el if en menu
            elif eleccion == "n":
                return False

    def update_cliente(self):
        while True:
            self.limpiarconsola()
            print("Modificar un cliente:")
            rut = self.ValidarRut()
            if rut == "":
                break
            cliente = manager.r_cliente_one(rut)
            if not cliente:
                print("El rut no existe")
                return
            self.limpiarconsola()
            print("Cliente encontrado:")
            dbprint.print_clientes([cliente], False)
            campos = list(cliente)
            new_cliente = cliente.copy()
            cantidad_cambios = 0
            for campo in campos:
                campo_legible = str(campo).replace("_", " ").capitalize()
                if campo == "_id":
                    continue
                opcion = input(
                    "¿Deseas modificar el campo {}? (s/N):".format(campo_legible)
                )
                if opcion == "s":
                    cantidad_cambios += 1
                    print(
                        "El valor actual de {} es {}".format(
                            campo_legible, cliente[campo]
                        )
                    )
                    if campo == "fecha_registro":
                        valor = self.ValidarFecha()
                        if valor:
                            new_cliente[campo] = valor

                    elif campo == "telefono":
                        valor = self.ValidarTelefono()
                        if valor:
                            new_cliente[campo] = valor
                    else:
                        new_cliente[campo] = input("Ingresa el nuevo valor:")
                elif opcion == "":
                    continue
                else:
                    print("Ingresa una opción correcta (s/n)")
            self.limpiarconsola()
            if cantidad_cambios == 0:
                print("No realizaste ningún cambio")
                input("Presiona Enter para volver al menu...")
                break
            print("Cliente original:")
            dbprint.print_clientes([cliente], False)
            print("Hay {} cambios a realizar:".format(str(cantidad_cambios)))
            dbprint.print_clientes([new_cliente], False)
            input("Presiona enter para continuar")
            self.limpiarconsola()
            manager.u_cliente(new_cliente)
            break

    def delete_cliente(self):
        self.limpiarconsola()
        rut = self.ValidarRut()
        manager.d_cliente(rut)
        self.continuar()

    def ValidarTelefono(self):
        while True:
            try:
                regex_tel = re.compile("^\\+569\\d{8}$")
                telefono = input("Ingrese telefono: +569")
                telefono = telefono.strip()
                if not telefono:
                    return False
                telefono = "+569" + telefono
                if regex_tel.match(telefono):
                    return telefono
                else:
                    print("Ingrese un teléfono válido")
            except Exception as e:
                print(e)

    def ValidarCorreo(self):
        pass

    def ValidarFecha(self):
        while True:
            try:
                fecha_registro = input(
                    "Ingrese fecha de registro(Formato AAAA-MM-DD, incluya guión): "
                )
                if fecha_registro == "":
                    return False
                fecha_registro = fecha_registro.strip()
                fecha_registro = datetime.strptime(
                    fecha_registro, "%Y-%m-%d"
                )  # lanza value error si el formato es incorrecto o la fecha es inválida, no hace falta un raise
                return fecha_registro
            except ValueError:
                print("Ingrese una fecha válida")

    def ValidarRut(self):
        rutValido = ""
        while rutValido == "":
            try:
                regex_rut = re.compile("^\\d{8}-\\d$")
                print("Si desea cancelar la operación escriba exit y presione Enter")
                rut = input("Ingrese RUT del cliente (sin puntos y con guión): ")
                while rut == "":
                    rut = input("Ingrese RUT del cliente (sin puntos y con guión): ")
                if rut == "exit":
                    return ""
                rut = rut.strip()
                if not regex_rut.match(rut):
                    print("Ingrese un RUT válido")
                else:
                    comprobacion = manager.r_comp_rut(rut)
                    if comprobacion:
                        rutValido = rut
                        return rutValido
                    else:
                        print("Rut no existe en la base de datos")
            except Exception as e:
                print(e)

    def create_pedido(self):
        print("(Pulse enter vacío para cancelar la operación)")
        productos_anadir = (
            []
        )  # usado para mostrar el resumen de los productos y añadirlos al pedido
        monto_total = (
            0  # usado para modificar el monto total del pedido al final del calculo
        )
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
                producto_elegido = next(
                    (p for p in lista_productos if p["numero_producto"] == seleccion),
                    None,
                )
                # usa el generador para recorrer toda la lista de productos filtrando con if si es que el número del producto corresponde a la selección
                # next pide al generador el primer elemento (producto) que coinicida con la condición if y detiene el generador cuando se cumple
                # en caso de que no haya ninguna coincidencia, el generador entrega None y pide realizar la seleccion otra vez
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
                        "producto_id": producto_elegido.get("_id"),
                        "nombre": producto_elegido.get("nombre"),
                        "cantidad": cantidad,
                        "precio": precio_total,
                    }
                    productos_anadir.append(producto_final)
                else:
                    print("Seleccione un producto válido")
                    self.continuar()
                    continue  # evita que se pregunte si se quiere añadir otro producto, evitando ingresar un pedido vacío al continuar con el loop saltandose las siguientes líneas
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

        if (
            not productos_anadir
        ):  # si la lista de productos está vacía, se evita que se siga creando el pedido (no debería ser posible pero sirve como otra barrera de seguridad)
            print("El pedido no puede estar vacío, cancelando..")
            self.continuar()
            return False
        dbprint.print_resumen_crear_pedido(productos_anadir, monto_total, rut)
        while True:
            eleccion = input("¿Desea crear el pedido?(S/N): ")
            eleccion = eleccion.strip().lower()
            if eleccion == "s":
                for (
                    producto
                ) in (
                    productos_anadir
                ):  # elimina el nombre del producto antes de insertarlo, solo fue usado para visualización
                    del producto["nombre"]
                manager.c_pedido(rut, monto_total, productos_anadir)
                self.continuar()
                self.limpiarconsola()
                return True
            elif eleccion == "n":
                return False
            else:
                print("Seleccione una opción válida")

    def delete_pedido(self):
        self.limpiarconsola()
        print("(Ingrese RUT del cliente para ver sus pedidos)")
        rut = self.ValidarRut()
        lista_pedidos = manager.r_pedidos_rut(rut)
        if not lista_pedidos:
            self.continuar()
            return False
        while True:
            dbprint.print_pedidos(
                lista_pedidos
            )  # esta función de print ya añade el índice seleccionable a la lista, por lo que no hace falta agregarlo aparte
            try:
                seleccion = int(input("Seleccione un pedido: "))
                pedido_elegido = next(
                    (p for p in lista_pedidos if p["numero_pedido"] == seleccion),
                    None,
                )
                if pedido_elegido:
                    id_pedido_elegido = pedido_elegido.get("_id")
                    break
                else:
                    print("Ingrese un pedido válido")
                    self.continuar()
            except ValueError:
                print("Ingrese un valor válido")
                self.continuar()

        while True:
            eleccion = input("¿Está seguro que quiere eliminar este pedido?(S/N): ")
            eleccion = eleccion.strip().lower()
            if eleccion == "s":
                manager.d_pedido(id_pedido_elegido)
                self.continuar()
                return True
            elif eleccion == "n":
                print("Cancelando operación..")
                self.continuar()
                return False
            else:
                print("Ingrese una opción válida")

    def create_producto(self):
        self.limpiarconsola()
        print("(Pulse enter vacío para cancelar la operación)")
        nombre = input("Ingrese nombre del producto que agregará: ")
        if not nombre:
            return False
        nombre = nombre.strip()

        while True:
            precio = input("Ingrese el precio del producto: ")
            if not precio:
                return False

            if (
                precio.isdigit()
            ):  # Esto es un metodo propio de python de las cadenas de texto
                precio = int(
                    precio
                )  # luegod e hacer todas las comprobaciones transformamos el precio en un int
                break
            else:
                print("Error. Debe ingresar un número entero válido")

        producto = {
            "nombre": nombre,
            "precio": precio,
        }
        print("Datos del Producto a añadir:")
        print(f"Nombre: {producto["nombre"]} | Precio: {producto["precio"]}")
        while True:
            eleccion = input("¿Quiere agregar este producto? (S/N): ")
            eleccion = eleccion.strip().lower()
            if eleccion == "s":
                manager.c_producto(producto)
                self.continuar()
                return True  # solo usarlo al final, evita que aparezca operación cancelada por el if en menu
            elif eleccion == "n":
                return False

    def update_anadir_producto_pedido(self):
        self.limpiarconsola()
        print("(Ingrese RUT del cliente para ver sus pedidos)")
        rut = self.ValidarRut()
        productos_anadir = []
        lista_pedidos = manager.r_pedidos_rut(rut)
        if not lista_pedidos:
            self.continuar()
            return False
        while True:
            dbprint.print_pedidos(
                lista_pedidos
            )  # esta función de print ya añade el índice seleccionable a la lista, por lo que no hace falta agregarlo aparte
            try:
                seleccion = int(input("Seleccione un pedido: "))
                pedido_elegido = next(
                    (p for p in lista_pedidos if p["numero_pedido"] == seleccion),
                    None,
                )
                if pedido_elegido:
                    id_pedido_elegido = pedido_elegido.get("_id")
                    monto_total = int(pedido_elegido.get("monto_total"))
                    break
                else:
                    print("Ingrese un pedido válido")
                    self.continuar()
            except ValueError:
                print("Ingrese un valor válido")
                self.continuar()
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
                producto_elegido = next(
                    (p for p in lista_productos if p["numero_producto"] == seleccion),
                    None,
                )
                # usa el generador para recorrer toda la lista de productos filtrando con if si es que el número del producto corresponde a la selección
                # next pide al generador el primer elemento (producto) que coinicida con la condición if y detiene el generador cuando se cumple
                # en caso de que no haya ninguna coincidencia, el generador entrega None y pide realizar la seleccion otra vez
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
                        "producto_id": producto_elegido.get("_id"),
                        "nombre": producto_elegido.get("nombre"),
                        "cantidad": cantidad,
                        "precio": precio_total,
                    }
                    productos_anadir.append(producto_final)
                else:
                    print("Seleccione un producto válido")
                    self.continuar()
                    continue  # evita que se pregunte si se quiere añadir otro producto, evitando ingresar un pedido vacío al continuar con el loop saltandose las siguientes líneas
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

        if (
            not productos_anadir
        ):  # si la lista de productos está vacía, se evita que se siga creando el pedido (no debería ser posible pero sirve como otra barrera de seguridad)
            print("El pedido no puede estar vacío, cancelando..")
            self.continuar()
            return False

        while True:
            eleccion = input("¿Desea agregar los productos al pedido?(S/N): ")
            eleccion = eleccion.strip().lower()
            if eleccion == "s":
                for producto in productos_anadir:
                    del producto["nombre"]
                manager.u_pedido_anadir_productos(
                    id_pedido_elegido, monto_total, productos_anadir
                )
                self.continuar()
                return True
            elif eleccion == "n":
                print("Cancelando operación..")
                self.continuar()
                return False

    def update_eliminar_producto_pedido(self):
        self.limpiarconsola()
        print("(Ingrese RUT del cliente para ver sus pedidos)")
        rut = self.ValidarRut()
        lista_pedidos = manager.r_pedidos_rut(rut)
        if not lista_pedidos:
            self.continuar()
            return False
        while True:
            dbprint.print_pedidos(
                lista_pedidos
            )  # esta función de print ya añade el índice seleccionable a la lista, por lo que no hace falta agregarlo aparte
            try:
                seleccion = int(input("Seleccione un pedido: "))
                pedido_elegido = next(
                    (p for p in lista_pedidos if p["numero_pedido"] == seleccion),
                    None,
                )
                if pedido_elegido:
                    id_pedido_elegido = pedido_elegido.get("_id")
                    monto_total = int(pedido_elegido.get("monto_total"))
                    lista_productos_pedido = pedido_elegido.get("productos")
                    break
                else:
                    print("Ingrese un pedido válido")
                    self.continuar()
            except ValueError:
                print("Ingrese un valor válido")
                self.continuar()
        print("Ahora eligirá el producto a eliminar")
        self.continuar()
        if not lista_productos_pedido:
            self.continuar()
            return False
        for indice, producto in enumerate(lista_productos_pedido, start=1):
            producto["numero_producto"] = indice

        while True:
            dbprint.print_productos_disponibles(lista_productos_pedido)
            try:
                seleccion = int(input("Seleccione un producto: "))
                producto_elegido = next(
                    (
                        p
                        for p in lista_productos_pedido
                        if p["numero_producto"] == seleccion
                    ),
                    None,
                )
                if producto_elegido:
                    id_producto_elegido = producto_elegido.get("producto_id")
                    precio_producto = producto_elegido.get("precio")
                    monto_total -= precio_producto
                    break
                else:
                    print("Seleccione un producto válido")
                    self.continuar()
            except ValueError:
                print("Ingrese un valor válido")
                self.continuar()

        while True:
            eleccion = input(
                "¿Está seguro que quiere eliminar el producto de este pedido?(S/N): "
            )
            eleccion = eleccion.lower().strip()
            if eleccion == "s":
                manager.u_pedido_eliminar_productos(
                    id_pedido_elegido, monto_total, id_producto_elegido
                )
                self.continuar()
                return True
            elif eleccion == "n":
                print("Cancelando operación..")
                return False
            else:
                print("Seleccione una opción válida")

    def eliminar_producto(self):
        self.limpiarconsola()
        print("(Pulse enter vacío para cancelar la operación)")
        nombre = input("Ingrese nombre del producto para eliminar: ")
        nombre = nombre.strip()
        if not nombre:
            return False

        comprobacion = manager.comprobar_producto(nombre)
        if comprobacion:
            while True:
                eleccion = input(
                    f"¿Está seguro que quiere eliminar el producto '{nombre}' del catálogo? (S/N): "
                )
                eleccion = eleccion.lower().strip()
                if eleccion == "s":
                    manager.bd_eliminar_producto(nombre)
                    self.continuar()
                    return True
                elif eleccion == "n":
                    return False
                else:
                    print("Seleccione una opción válida (S o N)")
        else:
            self.continuar()
            return False

    def update_editar_producto(self):
        self.limpiarconsola()
        lista_productos = manager.r_productos_anadir_pedido()
        if not lista_productos:
            self.continuar()
            return False
        for indice, producto in enumerate(lista_productos, start=1):
            producto["numero_producto"] = indice

        while True:
            dbprint.print_productos_disponibles(lista_productos)
            try:
                seleccion = int(input("Seleccione un producto: "))
                producto_elegido = next(
                    (p for p in lista_productos if p["numero_producto"] == seleccion),
                    None,
                )
                if producto_elegido:
                    id_producto_elegido = producto_elegido.get("_id")
                    nombre = producto_elegido.get("nombre")
                    precio = producto_elegido.get("precio")
                    break
                else:
                    print("Seleccione un producto válido")
                    self.continuar()
                    continue 
            except ValueError:
                print("Ingrese un valor válido")
                self.continuar()
                continue
        
        otro = True
        while otro:
            self.limpiarconsola()
            print("1. Editar Nombre")
            print("2. Editar Precio")
            eleccion = input("Ingrese campo a editar: ")
            eleccion = eleccion.strip()
            if eleccion == "1":
                while True:
                    nombre = input("Ingrese nuevo nombre: ")
                    nombre = nombre.strip()
                    if not nombre:
                        print("No puede ingresar un nombre vacío")
                    else:
                        break
            elif eleccion == "2":
                while True:
                    try:
                        precio = int(input("Ingrese un nuevo precio: "))
                        if precio < 1:
                            print("Ingrese un valor válido")
                        else:
                            break
                    except ValueError:
                        print("Ingrese un valor válido")
            else:
                print("Ingrese una opción válida")
                continue

            while True:
                seguir = input("¿Quiere editar otro campo?(S/N): ")
                seguir = seguir.lower().strip()
                if seguir == "s":
                    otro = True
                    break
                elif seguir == "n":
                    otro = False
                    break
                else:
                    print("Seleccione una opción válida")

        while True:
                eleccion = input("¿Confirma la edición del producto?(S/N): ")
                eleccion = eleccion.lower().strip()
                if eleccion == "s":
                    editar = manager.u_editar_producto(id_producto_elegido, nombre, precio)
                    self.continuar()
                    return False
                elif eleccion == "n":
                    print("Cancelando operación..")
                    return False
                else:
                    print("Seleccione una opción válida")
