"""
# Aplicación foliadora de archivos PDF.
Reconoce los siguientes argumentos:

 - por_fecha, por_nombre: ordenamientos, por omisión es por_nombre
 - solo_orden: argumento para detener el proceso luego de describir el orden

Usa los siguientes directorios:

 - `pdfs-sin-foliar/`: archivos originales pendientes de foliar
 - `pdfs-procesados/`: archivos originales ya foliados
 - `pdfs-foliados/`: archivos nuevos con páginas foliadas

 Los archivos a sellar que son originales se toman de la carpeta `pdfs-sin-foliar` y luego 
 se mueven a `pdfs-procesados`.

 Se escriben los siguientes archivos:

  - `historial.txt`: registro de archivos procesados con la secuencia inicial.
  - `foliado.txt`: registro del siguiente sello.

"""
import os
from shutil import move
import reportlab
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from PyPDF2 import PdfFileWriter, PdfFileReader

def lista_archivos_ordenados(orden):
    """
        Obtiene los archivos a procesar con el orden indicado. Devuelve una lista de nombres.
        - orden: por_fecha, por_nombre (valor por defecto)
    """
    lista_archivos=[]
    if orden=="por_fecha":
        from pathlib import Path
        files = sorted(Path("pdfs-sin-foliar").iterdir(), key=os.path.getmtime)
        if len(files)>0:
            print("archivos ordenados por fecha")
            lista_archivos=[file.name for file in files]
            primero,ultimo=files[0],files[-1]
            print(f"primer archivo: {primero.name}")
            print(f"último archivo: {ultimo.name}")
    else:
        lista_archivos=sorted(os.listdir("pdfs-sin-foliar"))
        if len(lista_archivos)>0:
            print("archivos ordenados por nombre")
            primero,ultimo=lista_archivos[0],lista_archivos[-1]
            print(f"primer archivo: {primero}")
            print(f"último archivo: {ultimo}")
    
    return lista_archivos


def secuencia_obtiene():
    """
        Obtiene la secuencia almancenada en el archivo `foliado.txt`,
        devuelve un par ordenado: (clase,secuencia).
    """
    clase_docs = "Ninguno"
    secuencia = 1    
    try:
        file1 = open("foliado.txt","r") 
        texto = file1.readline()
    except:
        texto = f"{clase_docs} {secuencia}"
        print("Archivo foliado.txt no encontrado o con contenido inválido")
    if " - " in texto:
        clase_docs=texto.split(" - ")[0]
        secuencia=int(texto.split(" - ")[1])
    elif " " in texto:
        clase_docs=texto.split(" ")[0]
        secuencia=int(texto.split(" ")[1])

    return clase_docs, secuencia



def secuencia_actualiza(clase_docs:str,secuencia:int):
    """
        Escribe el siguiente sello en el archivo `foliado.txt`.
    """
    try:
        with open('foliado.txt', 'w') as file1:
            file1.write(f"{clase_docs} - {secuencia}")
            print(f"siguiente sello: {clase_docs} - {secuencia}")
    except:
        print("Archivo foliado.txt no encontrado o con contenido inválido")



def pdf_imprime_sellos(num, tmp, clase_docs, secuencia):
    """
        Imprime los sellos con la secuencia en hojas limpias, usa archivo temporal.
    """
    lienzo = canvas.Canvas(tmp)
    for i in range(0,num): 
        # lienzo.rotate(90)
        lienzo.setFont("Helvetica", 20)
        lienzo.setFillColorRGB(0, 0, 0.77)
        # lienzo.drawString((5)*mm, (-5)*mm, clase_docs + " - " + str(i+secuencia)) # izquierda abajo paralelo-lado
        # lienzo.drawString(0, 0, clase_docs + " - " + str(i+secuencia)) # izquierda abajo paralelo-abajo
        lienzo.setFont("Helvetica",20)
        lienzo.rotate(90)
        lienzo.drawString((50)*mm, (-150)*mm, clase_docs + " - " + str(i+secuencia))
        lienzo.showPage()
    lienzo.save()



def pdf_mueve(nombre):
    """
        Mueve el archivo procesado fuera del directorio de trabajo en la carpeta
        `pdfs-procesados`.
    """
    if not os.path.isdir("pdfs-procesados/"):
        os.mkdir("pdfs-procesados/")
    path1 = os.path.join("pdfs-sin-foliar", nombre)
    path2 = os.path.join("pdfs-procesados", nombre)
    move(path1, path2)


def historial_de_procesado_agrega(secuencia,nombrearchivo):
    """
        Agrega al historial el archivo de procesados.
    """
    try:
        with open('historial.txt', 'a') as file1:
            file1.write(str(secuencia)+" "+nombrearchivo+"\n")
    except:
        print("Archivo historial.txt no encontrado o con contenido inválido")



if __name__ == "__main__":
    import sys
    tmp = "__tmp.pdf"
    argv = sys.argv
    ordenamiento="por_nombre"
    solo_orden=False
    if "por_fecha" in argv:
        ordenamiento="por_fecha"
    solo_orden = "solo_orden" in argv
    
    (clase_docs,secuencia) = secuencia_obtiene()
    lista_archivos=lista_archivos_ordenados(ordenamiento)

    if len(lista_archivos)==0:
        print("sin archivos para foliar")
    if solo_orden:
        exit()

    output = PdfFileWriter()
    for filename in lista_archivos:
        base = os.path.basename(filename)
        path = os.path.join("pdfs-sin-foliar", filename)
        if os.path.isdir(path):
            # saltar directorios
            continue
        if filename.endswith('.pdf'):
            with open(path, "rb") as f:
                print(f"inicia con archivo {filename}")
                historial_de_procesado_agrega(secuencia, filename)
                pdf = PdfFileReader(f, strict=False)
                n = pdf.getNumPages()
                pdf_imprime_sellos(n, tmp, clase_docs, secuencia)
                secuencia=secuencia+n

                if not os.path.isdir("pdfs-foliados/"):
                    os.mkdir("pdfs-foliados/")
                with open(tmp, "rb") as ftmp:
                    numberPdf = PdfFileReader(ftmp)
                    newpath = "pdfs-foliados/"+ base
                    with open(newpath, "wb") as f:
                        output.write(f)
                    output = PdfFileWriter()
                    for p in range(n):
                        print(f"hoja: {p+1} de {n}")
                        page = pdf.getPage(p)
                        numberLayer = numberPdf.getPage(p)
                        
                        page.mergePage(numberLayer)
                        output.addPage(page)
                    if output.getNumPages():
                        newpath = "pdfs-foliados/" + base
                        with open(newpath, "wb") as f:
                            output.write(f)            
                os.remove(tmp)
            pdf_mueve(filename)
            print(f"termina con archivo {filename}")

    if len(lista_archivos)>0:
        secuencia_actualiza(clase_docs, secuencia)        
        print("Fin del proceso")
    else:
        print("no hubo archivos para foliar")
