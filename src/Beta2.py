"""
PROCESO: 40%

# Informacion del proyecto

   Nombre del proyecto: BNotepad
   Inicio del proyecto: 23/06/2022

   Version: 1.0 (Beta Dev Version)
   License: 

   Developer: Alvaro (Baqueto | SKEYLODA) 


## Sobre el proyecto:

   Librerias utilizadas:

      PyQt5 -> GUI python library builded with Ctypes (C++ implementation)
      Docs | Guide -> https://doc.bccnsoft.com/docs/PyQt5/
"""

#* Interprete del sistema por defecto (ejecuta la aplicacion en la direccion de memoria (0x00000400 segun CPython)
import sys
import os
import zipfile
from  werkzeug.security import *

from descinfo import *

from PyQt5.QtWidgets import (QApplication, QMainWindow, QAction, QMessageBox, QTextEdit,
QFileDialog, QInputDialog, QFontDialog, QColorDialog)

from PyQt5.QtGui import QIcon,QTextCursor, QColor, QFont
from PyQt5.QtCore import Qt


# TODO: POR TERMINAR (al 20%)
class Compressor:

   def __init__(self, path: os.path, system = ["Mac", "Windows", "Linux"]):
      self.system: str = system
      try:
         self.path: os.path = path
      except os.error:
         return f"El parametro 'path' no posee un formato valido. Proporciona una ruta de sistema"
      
   def Compress(self,compression_destination: os.path, compress_method = ["DEFLATED", "BZIP2", "LZMA"]):
      """Comprime un archivo en distintos metodos de compresion.\n
      Los permitidos son:\n
      ``"""
      for m in compress_method:
         if m == "DEFLATED":
            self.method = zipfile.ZIP_DEFLATED
         elif m == "BZIP2":
            self.method = zipfile.ZIP_BZIP2
         elif m == "LZMA":
            self.method = zipfile.ZIP_LZMA
            
      archive = zipfile.ZipFile(self.path, 'w')
      archive.write(compression_destination, compress_type=self.method)
      archive.close()
      return archive

   def CompressGroup(self, file_type = [".pdf", ".png", ".jpeg", "*"]):
      zipper = zipfile.ZipFile(self.path, 'w')
      
      for folder, subfolders, files in os.walk(self.path):
         for file in files:
            if file.endswith('.pdf'):
                  zipper.write(os.path.join(folder, file), os.path.relpath(os.path.join(folder,file), self.path), compress_type = zipfile.ZIP_DEFLATED)
      
      zipper.close()


# TODO: NO TERMINADO (PROPENSO A MUCHOS FALLOS)
class Notepad(QMainWindow):

   def __init__(self):
      super().__init__()

      self.initializeUI()
      #* Colocamos un atributo para saber si un archivo esta abierto o no
      self.FileOpened: list[bool | str] = [False, ""]

   def initializeUI(self):
         """Inicializa la ventana e inicializa tambien todos los widgets de la aplicacion"""
         self.x = 750
         self.y = 500
         self.setGeometry(600, 400, self.x, self.y)
         self.setStyleSheet(
            """
            QTextEdit {border: 1px flex black}
            """
         )

         self.setWindowTitle('BNotePad')
         self.setWindowIcon(QIcon(r'images\NotePadIcon.png'))
         #* Cargamos el widget al compilador de la libreria
         self.createNotepadWidget()
         #* Cargamos el menu al sys.argv()
         self.notepadMenu()
         #* Cargamos todo y lo mostramos. Deberemos utilizar OpenGL para ello.
         self.show()

   def createNotepadWidget(self):
         """
         Configura el widget central (lo posiciona).\n
         Para la clase ``QmainWindow``, que es la clase ``QTextEditWidget`` para el notepad
         """
         self.text_field = QTextEdit()

         #* Editamos la interfaz del texto y configuramos algunos parametros nativos 
         #* (como constantes, pero nativos es como llama C++ a los parametros que se inician con la app)
         self.text_field.setPlaceholderText("Escriba texto aqui")
         self.text_field.setFont(QFont("Roboto Condensed", 12, 0))
         #* Pasamos el widget al compliador para que lo coloque en la app
         self.setCentralWidget(self.text_field)

   def notepadMenu(self):
      #TODO: Create menu for notepad GUI
      #*Creamos las acciones para el menu

      new_act=QAction(QIcon(r'images\new_file.png'),'New',self)
      new_act.setShortcut('Ctrl+N')
      new_act.triggered.connect(self.clearText)

      open_act=QAction(QIcon(r'images\open_file.png'),'Open',self)
      open_act.setShortcut('Ctrl+O')
      open_act.triggered.connect(self.openFile)

      fileinfo_act=QAction(QIcon(r'images\file_info.png'),'FileInfo',self)
      fileinfo_act.setShortcut('Ctrl+Shift+F')
      fileinfo_act.triggered.connect(self.ShowFileInfo)

      save_act=QAction(QIcon(r'images\save_file.png'),'Save',self)
      save_act.setShortcut('Ctrl+S')
      save_act.triggered.connect(self.saveToFile)

      exit_act=QAction(QIcon(r'images\exit.png'),'Exit',self)
      exit_act.setShortcut('Ctrl+Q')
      exit_act.triggered.connect(self.exitApp)


      #* Create actions for edit menu

      undo_act=QAction(QIcon(r'images\undo.png'),"Undo",self)
      undo_act.setShortcut('Ctrl+Z')
      undo_act.triggered.connect(self.text_field.undo)

      redo_act=QAction(QIcon(r'images\redo.png'),'Redo',self)
      redo_act.setShortcut('Ctrl+Shift+Z')
      redo_act.triggered.connect(self.text_field.redo)

      cut_act=QAction(QIcon(r'images\cut.png'),'Cut',self)
      cut_act.setShortcut('Ctrl+X')
      cut_act.triggered.connect(self.text_field.cut)

      copy_act=QAction(QIcon(r'images\copy.png'),'Copy',self)
      copy_act.setShortcut('Ctrl+C')
      copy_act.triggered.connect(self.text_field.copy)

      paste_act=QAction(QIcon(r'images\paste.png'),'Paste',self)
      paste_act.setShortcut('Ctrl+V')
      paste_act.triggered.connect(self.text_field.paste)

      find_act=QAction(QIcon(r'images\find.png'),'Find',self)
      find_act.setShortcut('Ctrl+F')
      find_act.triggered.connect(self.findTextDialog)


      #* Tool bar actions menu

      font_act=QAction(QIcon(r'images\font.png'),'Font',self)
      font_act.setShortcut('Ctrl+T')
      font_act.triggered.connect(self.chooseFont)

      color_act=QAction(QIcon(r'images\font_color.png'),'Color',self)
      color_act.setShortcut('Ctrl+Shift+C')
      color_act.triggered.connect(self.chooseFontColor)

      highlight_act=QAction(QIcon(r'images\highlight.png'),'Highlight',self)
      highlight_act.setShortcut('Ctrl+Shift+H')
      highlight_act.triggered.connect(self.chooseFontBackgroundColor)

      #* Create MenuBar
      menu_bar = self.menuBar()
      menu_bar.setNativeMenuBar(False)

      #* Create file menu and add actions
      file_menu = menu_bar.addMenu("File")
      file_menu.addAction(new_act)
      file_menu.addSeparator()
      file_menu.addAction(open_act)
      file_menu.addAction(save_act)
      file_menu.addAction(fileinfo_act)
      file_menu.addSeparator()
      file_menu.addAction(exit_act)

      #* Create edit menu and add actions
      edit_menu = menu_bar.addMenu("Edit")
      edit_menu.addAction(undo_act)
      edit_menu.addAction(redo_act)
      edit_menu.addAction(cut_act)
      edit_menu.addAction(copy_act)
      edit_menu.addAction(paste_act)
      edit_menu.addSeparator()
      edit_menu.addAction(find_act)
      edit_menu.addAction(fileinfo_act)

      #* Create tool menu and add actions
      tool_menu = menu_bar.addMenu("Tool")
      tool_menu.addAction(font_act)
      tool_menu.addAction(color_act)
      tool_menu.addAction(highlight_act)
      tool_menu.addSeparator()

      #* Create settings menu

      BackgroundColor_act = QAction(QIcon(r'Images\BackgroundColor.png'), "IDE Color" ,self)
      BackgroundColor_act.setShortcut('Ctrl+Shift+I')
      BackgroundColor_act.triggered.connect(self.setBackgroundColor)

      settings_act = QAction(QIcon(r'Images\settings.png'), "Preferences" ,self)
      settings_act.setShortcut('Ctrl+Shift+P')
      settings_act.triggered.connect(self.settings)

      settings_menu = menu_bar.addMenu("Settings")
      settings_menu.addAction(BackgroundColor_act)
      settings_menu.addAction(settings_act)

      #* Create help menu
      about_act=QAction(QIcon(r'Images\about.png'), 'About',self)
      about_act.setShortcut('Ctrl+Shift+A')
      about_act.triggered.connect(self.aboutDialog)

      devinfo_act=QAction('DevInfo',self)
      devinfo_act.setShortcut('Ctrl+Shift+D')
      devinfo_act.triggered.connect(self.devInfo)

      help_menu=menu_bar.addMenu('Help')
      help_menu.addAction(about_act)
      help_menu.addAction(devinfo_act)


   def openFile(self):
      """
      Abre un archivo dentro de los permitidos y vuelca todo su contenido en el text field
      """

      file_name,_ = QFileDialog.getOpenFileName(
         self, 
         "Abrir archivo",
         initialFilter= "Text Files(*.txt)", 
         filter="Text Files(*.txt);;HTML Files(*.html);;;;Python Files(*.py);;All Files(*)"
      )
      
      if file_name:
         FileAskOpen = QMessageBox.question(
            self, 
            "Abrir archivo", 
            f"Esta seguro que desa abrir {file_name} ?", 
            buttons= QMessageBox.No ,
            defaultButton= QMessageBox.Yes
         )
         if FileAskOpen == QMessageBox.Yes:
            self.text_field.clear()
            self.FileOpened = [True, file_name]
            with open(file_name,'r')as f:
               notepad_text = f.read()
               self.text_field.setText(notepad_text)
               self.setWindowTitle(f"BNotePad - Editing {file_name}")
         else:
            QMessageBox.information(self, "File Action",
               "No se ha abierto ningun archivo", QMessageBox.Ok)
      else:
         QMessageBox.information(self, "File Error",
            "Error al abrir o acceder al archivo", QMessageBox.Ok)
      

   def saveToFile(self):
      """
      Funcion para guardar un archivo en funcion de si es una archivo ya abierto y creado antes o no.\n
      Si el archivo ya esta creado, sobreescribiremos el contenido del archivo con el del editor.\n
      Si edl archivo es nuevo, se guardara con el nombre ``'Untitled - BNotePad'.txt`` como extension por defecto de archivos.
      """

      
      if self.FileOpened[0]:
         index = self.FileOpened[1].find(".")
         ffilter = self.FileOpened[1][index:]
         if ffilter == ".py":
            ffilter = "Python Files(*.py)"
         elif ffilter == ".html":
            ffilter = "HTML Files(*.html)"
      ffilter = None

      file_name,_ =QFileDialog.getSaveFileName(self,'Guardar Archivo',
      "Untitled - BNotePad" if not self.FileOpened[0] else self.FileOpened[1], initialFilter= ffilter if ffilter else "Text Files(*.txt)" ,filter="HTML Files(*.html);;Text Files(*.txt);;MarkDown Files(*.md);;Python Files(*.py)")
      
      if _ and file_name:
   
         if file_name.endswith('.html'):
            notepad_richtext= self.text_field.toHtml()
            with open(file_name,'w') as f:
               f.write(notepad_richtext)
               with open(file_name, "a") as f:
                  f.write(f"\n\n\n{bmark}")
                  f.close()
            QMessageBox.information(self, "Guardado de archivos", f"El archivo {file_name} se ha guardado correctamente", buttons= QMessageBox.Ok)
         elif file_name.endswith('.md'):
            notepad_richtext= self.text_field.toMarkdown()
            with open(file_name,'w') as f:
               f.write(notepad_richtext)
               with open(file_name, "a") as f:
                  f.write(f"\n\n\n{bmark}")
                  f.close()
            QMessageBox.information(self, "Guardado de archivos", f"El archivo {file_name} se ha guardado correctamente", buttons= QMessageBox.Ok)
         else:
            notepad_text= self.text_field.toPlainText()
            with open(file_name,'w') as f:
               f.write(notepad_text)
               with open(file_name, "a") as f:
                  f.write(f"\n\n\n{bmark}")
                  f.close()
            QMessageBox.information(self, "Guardado de archivos", f"El archivo {file_name} se ha guardado correctamente", buttons= QMessageBox.Ok)
      else:
         QMessageBox.information(self,"Save Error",
            "No ha sido posible guardar el archivo o se ha rechazado la operacion", QMessageBox.Ok)

   def ShowFileInfo(self):
      QMessageBox.information(self, "Sobre el comando", "Este comando esta siendo desarollado. Intentalo mas tarde", buttons= QMessageBox.Ok, defaultButton= QMessageBox.Ok)


   def clearText(self):
      """
      Pregunta si desea borrar el texto del editor para crear un nuevo archivo de texto.
      """

      answer= QMessageBox.question(self,"Clear Text",
         "Desea eliminar texto actual y crear un nuevo archivo?", buttons= QMessageBox.No, defaultButton= QMessageBox.Yes)

      if answer == QMessageBox.Yes:
         self.text_field.clear()
      else:
         pass

   def findTextDialog(self):
      """
      Busca texto por revelancia en QTextEdit widget (area de texto)
      """

      #* Mostramos un cuadro de dialogo de entrada para obtener la palabra con la que empezar a buscar
      find_text,ok= QInputDialog.getText(self,"Buscar Texto","Find:")
      extra_selections=[]

      #*Aseguramos que el texto se pueda modificar
      if ok and not self.text_field.isReadOnly():
         #*Mueve el cursor al principio del texto
         self.text_field.moveCursor(QTextCursor.Start)
         color= QColor(Qt.yellow)
         #* Buscamos mas ocurriencias en el texto
         while(self.text_field.find(find_text)):
            #* Usamos ExtraSelection para guardar de color amarillo 
            #* todas las ocurriencias que estamos escontrando
            selection=QTextEdit.ExtraSelection()
            selection.format.setBackground(color)
            #* Coloca el cursor sobre la ocurriencia
            selection.cursor=self.text_field.textCursor()
            #* Añadimos la ocurriencia a la lista
            extra_selections.append(selection)
         #*Subraya las ocurriencias en el widget de marco de texto (QTextEdit)
         for i in extra_selections:
            self.text_field.setExtraSelections(extra_selections)

   def chooseFont(self):
      """
      Seleccionar fuente para el texto
      """

      current=self.text_field.currentFont()

      font, ok= QFontDialog.getFont(current, self, options=QFontDialog.
      DontUseNativeDialog)

      if ok:
         self.text_field.setCurrentFont(font) #* Usar setFont() para colocar all todo el texto de esa fuente, de lo contrario, solo has 'setCurrentFont', para
         #* que a partir del cursor, la fuente sea esa

   def chooseFontColor(self):
      """
      Selecciona el color para el texto (color de fuente)
      """
      color=QColorDialog.getColor()

      if color.isValid():
         self.text_field.setTextColor(color)

   def chooseFontBackgroundColor(self):
      """
      Selecciona un subrayador para el texto.
      """
      color=QColorDialog.getColor()

      if color.isValid():
         self.text_field.setTextBackgroundColor(color)
      QColorDialog.getColor()


   def setBackgroundColor(self):
      QMessageBox.information(self, "Sobre el comando", "Este comando esta siendo desarollado. Intentalo mas tarde", buttons= QMessageBox.Ok, defaultButton= QMessageBox.Ok)

   def aboutDialog(self):
      """
      Muestra informacion sobre el programa mediante un cuadro de dialogo (void QMessageBox::InfoDialogBox -> Subclase de QDialog)
      """
      QMessageBox.about(self, "Sobre BNotepad", about)

   def devInfo(self):
      """
      Muestra informacion sobre el desarollo del programa mediante un cuadro de dialogo (void QMessageBox::InfoDialogBox -> Subclase de QDialog)
      """
      QMessageBox.about(self, "Sobre su desarollo", developermsg)

   def settings(self):
      """Muestra las preferencias guardadas en el programa. Toda esta info esta en la pila y el heap (memorias de C++) por defecto. Comando por desarollar de momento"""
      QMessageBox.information(self, "Sobre el comando", "Este comando esta siendo desarollado. Intentalo mas tarde", buttons= QMessageBox.Ok, defaultButton= QMessageBox.Ok)

   def exitApp(self):
      QMessageBox.question(self, "Salir del programa", "Esta seguro de que desea salir de BNotePad?", buttons= QMessageBox.No | QMessageBox.Yes, defaultButton= QMessageBox.No)


if __name__ == "__main__":
   #* Pasamos el ejecutable que ha creado el compilador automaticamente a la clase 'QApplication' y con 'sys.argv' lo empequetamos como una lista de argumentos
   #* al estilo setup.py con setuptools
   app= QApplication(sys.argv)
   #* Creamos un objeto NotePad (con los argumentos que ya hemos pasado a la clase 'QAplication' (Variables de entorno publicas por defecto por PYQt5 (C++)))
   window= Notepad()
   #* Mandamos que se ejecute la app (por ciclos) hasta que reciba una orden de cerrar (evento) y la aplicacion será cerrada
   sys.exit(app.exec())








