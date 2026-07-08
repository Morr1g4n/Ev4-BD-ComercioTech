from controlador.controladores import Controladores
from controlador.controladores import manager

controlador = Controladores()


class Menu:
    def menuInicial(self):
        controlador.limpiarconsola()
        while True:
            print("-" * 5 + "Gestor Admin ComercioTech" + "-" * 5)
            print("1.- Gestión Clientes")
            print("2.- Gestión Pedidos")
            print("3.- Gestión Productos")
            print("4.- Configurar base de datos (precargar datos y crear colecciones)")
            print("0.- Salir")
            eleccion = input("Elija una opción: ")
            if eleccion == "1":
                self.menuClientes()
            elif eleccion == "2":
                self.menuPedidos()
            elif eleccion == "3":
                self.menuProductos()
            elif eleccion == "4":
                controlador.limpiarconsola()
                manager.setup()
            elif eleccion == "0":
                print("Adiós!")
                raise SystemExit
            else:
                controlador.limpiarconsola()
                print("Seleccione una opción válida")

    def menuClientes(self):
        controlador.limpiarconsola()
        while True:
            print("-" * 5 + "Gestor Clientes" + "-" * 5)
            print("1.- Crear cliente")
            print("2.- Ver clientes")
            print("3.- Actualizar datos cliente")
            print("4.- Eliminar cliente")
            print("0.- Volver atrás")
            eleccion = input("Elija una opción: ")
            if eleccion == "1":
                crear = controlador.create_cliente()
                if not crear:
                    print("Operación cancelada")
            elif eleccion == "2":
                controlador.read_clientes_todos()
            elif eleccion == "3":
                pass
            elif eleccion == "4":
                controlador.delete_cliente()
            elif eleccion == "0":
                self.menuInicial()
            else:
                controlador.limpiarconsola()
                print("Seleccione una opción válida")

    def menuPedidos(self):
        controlador.limpiarconsola()
        while True:
            print("-" * 5 + "Gestor Pedidos" + "-" * 5)
            print("1.- Crear pedido")
            print("2.- Ver pedidos")
            print("3.- Agregar producto a un pedido")
            print("4.- Eliminar producto de un pedido")
            print("5.- Eliminar pedido")
            print("0.- Volver atrás")
            eleccion = input("Elija una opción: ")
            if eleccion == "1":
                crear = controlador.create_pedido()
                if not crear:
                    print("Operación cancelada")
            elif eleccion == "2":
                controlador.read_pedidos_todos()
            elif eleccion == "3":
                pass
            elif eleccion == "4":
                pass
            elif eleccion == "5":
                eliminar = controlador.delete_pedido()
                if not eliminar:
                    print("Operación cancelada")
            elif eleccion == "0":
                self.menuInicial()
            else:
                controlador.limpiarconsola()
                print("Seleccione una opción válida")

    def menuProductos(self):
        controlador.limpiarconsola()
        while True:
            print("-" * 5 + "Gestor Productos" + "-" * 5)
            print("1.- Crear producto")
            print("2.- Ver productos")
            print("3.- Editar producto")
            print("4.- Eliminar producto")
            print("0.- Volver atrás")
            eleccion = input("Elija una opción: ")
            if eleccion == "1":
                crear = controlador.create_producto()
                if not crear:
                    print("Operación cancelada")
            elif eleccion == "2":
                controlador.read_productos_todos()
            elif eleccion == "3":
                pass
            elif eleccion == "4":
                pass
            elif eleccion == "0":
                self.menuInicial()
            else:
                controlador.limpiarconsola()
                print("Seleccione una opción válida")
