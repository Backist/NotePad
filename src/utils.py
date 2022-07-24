from PIL import ImageTk, Image


def load_img(path, size): 
        return ImageTk.PhotoImage(Image.open(path).resize(size, Image.ANTIALIAS))  


def align_window(ventana, app_width, app_height):    
    pantall_ancho = ventana.winfo_screenwidth()
    pantall_largo = ventana.winfo_screenheight()
    x = int((pantall_ancho/2) - (app_width/2))
    y = int((pantall_largo/2) - (app_height/2))
    return ventana.geometry(f"{app_width}x{app_height}+{x}+{y}")


