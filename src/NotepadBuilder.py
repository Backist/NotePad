"""
Primera version del BNotePad.

Tkinter no es una GUI tan potente como PyQt5, lo cual he reescrito el programa con PyQt5 de acuerdo con los documentos
"""


from descinfo import *
from utils import *

from tkinter import *
from tkinter import messagebox
from tkinter.messagebox import *
from tkinter.filedialog import *

import re
import os


class Notepad:

    __root = Tk()
    __width: int = 300
    __height: int = 300
    __textarea = Text(__root)
    __menubar = Menu(__root)
    __filemenu = Menu(__menubar, tearoff=0)
    __editmenu = Menu(__menubar, tearoff=0)
    __helpmenu = Menu(__menubar, tearoff=0)
    __settingsmenu = Menu(__menubar, tearoff=0)
    __scrollbar = Scrollbar(__textarea)
    __file = None

    def __init__(self, width: int = 650, height:int = 650, **kwargs):

        #* Colocamos el icono con 'wm.iconbitmap'
        #try:
        #    self.__root.wm_iconbitmap("NotePad\NotePad.ico")
        #except KeyError or TclError:
        #    pass

        self.__width = width
        self.__height = height
            
        
        self.__root.title("Beta BNotePad")

        #* Centramos la ventana
        align_window(self.__root, self.__width, self.__height)

        self.__root.grid_rowconfigure(0, weight=1)
        self.__root.columnconfigure(0, weight=1)

        self.__textarea.grid(sticky= N + E + S + W)
        self.__textarea.config(font= ("Poppins", 12))

        self.__filemenu.add_command(label= "New", command= self.__newfile)
        self.__filemenu.add_command(label= "Open", command= self.__openfile)
        self.__filemenu.add_command(label= "Save", command= self.__savefile)
        self.__filemenu.add_command(label= "File info", command= self.__fileinfo)
        self.__filemenu.add_separator()
        self.__filemenu.add_command(label= "Exit", command= self.__quitapp)

        self.__editmenu.add_command(label= "Cut", command= self.__cut)
        self.__editmenu.add_command(label= "Copy", command= self.__copy)
        self.__editmenu.add_command(label= "Paste", command= self.__paste)

        self.__helpmenu.add_command(label="About", command= self.__showabout)
        self.__helpmenu.add_command(label="Developing", command= self.__showdev)
        self.__helpmenu.add_separator()
        self.__helpmenu.add_command(label= "Other Tools", command= self.__showtools)

        self.__settingsmenu.add_command(label="Settings", command= self.__settings)

        self.__menubar.add_cascade(label= "File", menu= self.__filemenu)
        self.__menubar.add_cascade(label= "Edit", menu= self.__editmenu)
        self.__menubar.add_cascade(label= "Help", menu= self.__helpmenu)
        self.__menubar.add_cascade(label= "Settings", menu= self.__settingsmenu)


        self.__root.config(menu= self.__menubar)
        self.__scrollbar.pack(side= RIGHT, fill= Y)

    def __quitapp(self):
        self.__root.destroy()
    
    def __showabout(self):
        showinfo("Sobre BNote Pad", message= about)

    def __fileinfo(self):

        if self.__file is None:
            messagebox.askretrycancel("File Error", "No hay ningun archivo abierto. Por favor, abra un archivo e intentelo de nuevo")
        else:
            file = open(self.__file, "r")
            self.__finfo = {}
            self.__finfo["Nombre"] = file.name
            self.__finfo["Encoding"] = file.encoding
            self.__finfo["Buffer"] = file.buffer
            for i,v in self.__finfo.items():
                finfo = f"""| {i} | -> {v}\n"""
            messagebox.showinfo("Sobre el archivo", message= finfo)

    def __openfile(self):
        self.__file = askopenfilename(defaultextension= ".txt", filetypes= [("All files", "*.*"), ("Text Documents", "*.txt*")])

        if self.__file == "":
            self.__file = None
        else:
            self.__root.title(os.path.basename(self.__file) + " - BNotePad")
            self.__textarea.delete(1.0, END)
            file = open(self.__file, "r")
            self.__textarea.insert(1.0, file.read())
            file.close()
    
    def __newfile(self):
        self.__root.title("Untitled - BNotePad")
        self.__file = None
        self.__textarea.delete(1,0, END)
    def __savefile(self):
        if self.__file is None:
            #* Guardamos el archivo como uno nuevo si no existe o no esta renombrado
            self.__file = asksaveasfilename(initialfile="Untitled.txt", defaultextension= ".txt", filetypes= [("All files", "*.*"), ("Text Documents", "*.txt*")])

            if self.__file is None:
                self.__file = None
            else:
                file = open(self.__file, "w")
                file.write(self.__textarea.get(1.0, END))
                file.close()
                #* Cerramos el archivo y lo volvermos a abrir para escribir la marca de agua
                file = open(self.__file, "a")
                file.write(bmark)
                file.close()
    
    def __showdev(self):
        showinfo("Sobre el desarollador", developermsg)
    
    def __showtools(self):
        showinfo("Herramientas adicionales", "Actualmente en desarollo")

    def __settings(self):
        showinfo("Ajustes del programa", "Actualmente en desarollo.\nSe creara otra ventana para establecer ajustes para la aplicacion")

    def __cut(self):
        self.__textarea.event_generate("<<Cut>>")
    
    def __copy(self):
        self.__textarea.event_generate("<<Copy>>")

    def __paste(self):
        self.__textarea.event_generate("<<Paste>>")

    def run(self):
        self.__root.mainloop()

if __name__ == "__main__":
    notepad = Notepad()
    notepad.run()


class Settings(Notepad):
    pass

        

