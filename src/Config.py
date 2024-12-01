from dataclasses import dataclass
from PyQt5.QtWidgets import QDialog, QWidget, QMessageBox

__all__ = ["SettingsDialog", "DataVault"]

class SettingsDialog(QWidget):

    def __init__(self, *args):
        super().__init__(*args)
        self.initializeDialog()

    def initializeWidget(self):
        """Inicializa los elementos de la interfaz y los elementos estaticos"""

        self.setWindowTitle("Preferencias")
        self.setGeometry(300, 300, 300, 200)
        self.setBackgroundRole()

    def CreateStaticElems(self):
        """Crea los elementos estaticos de la interfaz"""
        ...

    def DataVault(self):
        """Creamos una funcion para almacenar los datos de la interfaz"""

        d = DataVault()
        ...
    
    def show(self):
        """Mostramos la ventana"""
        super().show()


@dataclass()
class DataVault():

    MetaVault = {}

    def __init__(self):
        self.EntryDataEnabled: bool = True

    def insert(self, key, value):
        self.MetaVault[key] = value
    
    def getitem(self, key):
        return self.MetaVault[key]

    def toFormat(self):
        ...

