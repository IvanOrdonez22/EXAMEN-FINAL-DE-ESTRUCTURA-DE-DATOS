import sys
import json
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QLabel, QTextEdit, QWidget, QMessageBox, QTableWidgetItem, QTableWidget, QFileDialog

class Nodo:
    def __init__(self, id_estudiante, nombre, edad, calificacion):
        self.id_estudiante = id_estudiante
        self.nombre = nombre
        self.edad = edad
        self.calificacion = calificacion
        self.izquierda = None
        self.derecha = None

class ArbolBinarioBusqueda:
    def __init__(self):
        self.raiz = None

    def agregar_estudiante(self, id_estudiante, nombre, edad, calificacion):
        nuevo_nodo = Nodo(id_estudiante, nombre, edad, calificacion)
        if self.raiz is None:
            self.raiz = nuevo_nodo
        else:
            self._agregar(self.raiz, nuevo_nodo)

    def _agregar(self, nodo_actual, nuevo_nodo):
        if nuevo_nodo.id_estudiante < nodo_actual.id_estudiante:
            if nodo_actual.izquierda is None:
                nodo_actual.izquierda = nuevo_nodo
            else:
                self._agregar(nodo_actual.izquierda, nuevo_nodo)
        else:
            if nodo_actual.derecha is None:
                nodo_actual.derecha = nuevo_nodo
            else:
                self._agregar(nodo_actual.derecha, nuevo_nodo)

    def buscar_estudiante(self, id_estudiante):
        return self._buscar(self.raiz, id_estudiante)

    def _buscar(self, nodo_actual, id_estudiante):
        if nodo_actual is None:
            return None
        if nodo_actual.id_estudiante == id_estudiante:
            return nodo_actual
        elif id_estudiante < nodo_actual.id_estudiante:
            return self._buscar(nodo_actual.izquierda, id_estudiante)
        else:
            return self._buscar(nodo_actual.derecha, id_estudiante)

    def eliminar_estudiante(self, id_estudiante):
        self.raiz = self._eliminar(self.raiz, id_estudiante)

    def _eliminar(self, nodo_actual, id_estudiante):
        if nodo_actual is None:
            return nodo_actual

        if id_estudiante < nodo_actual.id_estudiante:
            nodo_actual.izquierda = self._eliminar(nodo_actual.izquierda, id_estudiante)
        elif id_estudiante > nodo_actual.id_estudiante:
            nodo_actual.derecha = self._eliminar(nodo_actual.derecha, id_estudiante)
        else:
            if nodo_actual.izquierda is None:
                return nodo_actual.derecha
            elif nodo_actual.derecha is None:
                return nodo_actual.izquierda

            temp = self._nodo_valor_minimo(nodo_actual.derecha)
            nodo_actual.id_estudiante = temp.id_estudiante
            nodo_actual.nombre = temp.nombre
            nodo_actual.edad = temp.edad
            nodo_actual.calificacion = temp.calificacion
            nodo_actual.derecha = self._eliminar(nodo_actual.derecha, temp.id_estudiante)

        return nodo_actual

    def _nodo_valor_minimo(self, nodo):
        actual = nodo
        while actual.izquierda is not None:
            actual = actual.izquierda
        return actual

    def listar_estudiantes_en_orden(self):
        estudiantes = []
        self._recorrido_en_orden(self.raiz, estudiantes)
        return estudiantes

    def _recorrido_en_orden(self, nodo, estudiantes):
        if nodo:
            self._recorrido_en_orden(nodo.izquierda, estudiantes)
            estudiantes.append((nodo.id_estudiante, nodo.nombre, nodo.edad, nodo.calificacion))
            self._recorrido_en_orden(nodo.derecha, estudiantes)

    def a_diccionario(self, nodo):
        if nodo is None:
            return None
        return {
            'id_estudiante': nodo.id_estudiante,
            'nombre': nodo.nombre,
            'edad': nodo.edad,
            'calificacion': nodo.calificacion,
            'izquierda': self.a_diccionario(nodo.izquierda),
            'derecha': self.a_diccionario(nodo.derecha)
        }

    def de_diccionario(self, datos):
        if datos is None:
            return None
        nodo = Nodo(datos['id_estudiante'], datos['nombre'], datos['edad'], datos['calificacion'])
        nodo.izquierda = self.de_diccionario(datos['izquierda'])
        nodo.derecha = self.de_diccionario(datos['derecha'])
        return nodo

class AplicacionGestionEstudiantes(QMainWindow):
    def __init__(self):
        super().__init__()
        self.arbol = ArbolBinarioBusqueda()
        self.initIU()

    def initIU(self):
        self.setWindowTitle('Sistema de Gestión de Estudiantes')
        self.setGeometry(100, 100, 800, 600)

        widget_central = QWidget()
        self.setCentralWidget(widget_central)

        layout = QVBoxLayout()

        layout_formulario = QFormLayout()
        self.entrada_id = QLineEdit()
        self.entrada_nombre = QLineEdit()
        self.entrada_edad = QLineEdit()
        self.entrada_calificacion = QLineEdit()
        layout_formulario.addRow('ID Estudiante:', self.entrada_id)
        layout_formulario.addRow('Nombre:', self.entrada_nombre)
        layout_formulario.addRow('Edad:', self.entrada_edad)
        layout_formulario.addRow('Calificación:', self.entrada_calificacion)

        self.boton_agregar = QPushButton('Agregar Estudiante')
        self.boton_agregar.clicked.connect(self.agregar_estudiante)
        layout_formulario.addWidget(self.boton_agregar)

        self.boton_eliminar = QPushButton('Eliminar Estudiante')
        self.boton_eliminar.clicked.connect(self.eliminar_estudiante)
        layout_formulario.addWidget(self.boton_eliminar)

        self.boton_buscar = QPushButton('Buscar Estudiante')
        self.boton_buscar.clicked.connect(self.buscar_estudiante)
        layout_formulario.addWidget(self.boton_buscar)

        self.boton_listar = QPushButton('Listar Estudiantes (Ascendente)')
        self.boton_listar.clicked.connect(self.listar_estudiantes)
        layout_formulario.addWidget(self.boton_listar)

        self.boton_actualizar_arbol = QPushButton('Actualizar Árbol')
        self.boton_actualizar_arbol.clicked.connect(self.actualizar_arbol)
        layout_formulario.addWidget(self.boton_actualizar_arbol)

        self.boton_guardar = QPushButton('Guardar Datos')
        self.boton_guardar.clicked.connect(self.guardar_datos)
        layout_formulario.addWidget(self.boton_guardar)

        self.boton_cargar = QPushButton('Cargar Datos')
        self.boton_cargar.clicked.connect(self.cargar_datos)
        layout_formulario.addWidget(self.boton_cargar)

        layout.addLayout(layout_formulario)

        self.etiqueta_informacion = QLabel()
        layout.addWidget(self.etiqueta_informacion)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(4)
        self.tabla.setHorizontalHeaderLabels(['ID', 'Nombre', 'Edad', 'Calificación'])
        layout.addWidget(self.tabla)

        self.etiqueta_arbol = QLabel('Árbol Binario de Búsqueda:')
        layout.addWidget(self.etiqueta_arbol)

        self.texto_arbol = QTextEdit()
        layout.addWidget(self.texto_arbol)

        widget_central.setLayout(layout)

    def agregar_estudiante(self):
        id_estudiante = int(self.entrada_id.text())
        nombre = self.entrada_nombre.text()
        edad = int(self.entrada_edad.text())
        calificacion = self.entrada_calificacion.text()
        self.arbol.agregar_estudiante(id_estudiante, nombre, edad, calificacion)
        QMessageBox.information(self, "Éxito", "Estudiante agregado exitosamente!")
        self.actualizar_arbol()

    def eliminar_estudiante(self):
        id_estudiante = int(self.entrada_id.text())
        self.arbol.eliminar_estudiante(id_estudiante)
        QMessageBox.information(self, "Éxito", "Estudiante eliminado exitosamente!")
        self.actualizar_arbol()

    def buscar_estudiante(self):
        id_estudiante = int(self.entrada_id.text())
        estudiante = self.arbol.buscar_estudiante(id_estudiante)
        if estudiante:
            QMessageBox.information(self, "Estudiante Encontrado", f"ID: {estudiante.id_estudiante}\nNombre: {estudiante.nombre}\nEdad: {estudiante.edad}\nCalificación: {estudiante.calificacion}")
        else:
            QMessageBox.warning(self, "No Encontrado", "Estudiante no encontrado!")

    def listar_estudiantes(self):
        self.tabla.clearContents()
        estudiantes = self.arbol.listar_estudiantes_en_orden()
        self.tabla.setRowCount(len(estudiantes))
        for fila, estudiante in enumerate(estudiantes):
            self.tabla.setItem(fila, 0, QTableWidgetItem(str(estudiante[0])))
            self.tabla.setItem(fila, 1, QTableWidgetItem(estudiante[1]))
            self.tabla.setItem(fila, 2, QTableWidgetItem(str(estudiante[2])))
            self.tabla.setItem(fila, 3, QTableWidgetItem(estudiante[3]))

    def actualizar_arbol(self):
        self.texto_arbol.clear()
        self.texto_arbol.setPlainText(self.obtener_estructura_arbol(self.arbol.raiz, ""))

    def obtener_estructura_arbol(self, nodo, prefijo):
        if nodo is None:
            return ""
        else:
            estructura_arbol = ""
            estructura_arbol += self.obtener_estructura_arbol(nodo.derecha, prefijo + "\t")
            estructura_arbol += prefijo + str(nodo.id_estudiante) + "\n"
            estructura_arbol += self.obtener_estructura_arbol(nodo.izquierda, prefijo + "\t")
            return estructura_arbol

    def guardar_datos(self):
        nombre_archivo, _ = QFileDialog.getSaveFileName(self, "Guardar Datos", "", "Archivos JSON (*.json)")
        if nombre_archivo:
            datos = self.arbol.a_diccionario(self.arbol.raiz)
            with open(nombre_archivo, 'w') as f:
                json.dump(datos, f)
            QMessageBox.information(self, "Éxito", "Datos guardados exitosamente!")

    def cargar_datos(self):
        nombre_archivo, _ = QFileDialog.getOpenFileName(self, "Cargar Datos", "", "Archivos JSON (*.json)")
        if nombre_archivo:
            with open(nombre_archivo, 'r') as f:
                datos = json.load(f)
            self.arbol.raiz = self.arbol.de_diccionario(datos)
            QMessageBox.information(self, "Éxito", "Datos cargados exitosamente!")
            self.actualizar_arbol()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = AplicacionGestionEstudiantes()
    ventana.show()
    sys.exit(app.exec())
#Ivan ordoñez
