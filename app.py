"""
# Aplicación foliadora de archivos PDF.

 Usa los siguientes directorios:

 - `pdfs-sin-foliar/`: archivos originales pendientes de foliar
 - `pdfs-procesados/`: archivos originales ya foliados
 - `pdfs-foliados/`: archivos nuevos con páginas foliadas

 Los archivos a sellar que son originales se toman de la carpeta `pdfs-sin-foliar` y luego 
 se mueven a `pdfs-procesados`.

 Se lee el siguiente archivo:
 
 - `foliado.txt`: registro del siguiente sello.

 Se escriben los siguientes archivos:

  - `historial.txt`: registro de archivos procesados con la secuencia inicial.
  - `foliado.txt`: registro del siguiente sello.

 En caso de excepción, en el historial queda el último archivo que se intentó abrir y procesar.

 Reconoce los siguientes argumentos:

 - `por_fecha`, `por_nombre`: ordenamientos, por omisión es por_nombre
 - `solo_orden`: argumento para detener el proceso luego de describir el orden
 - `no_consultar`: argumento para no consultar si debe realizarse el proceso luego
    de conocer el orden de los archivos.

"""
import os
import sys
from shutil import move
import reportlab
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from PyPDF2 import PdfFileWriter, PdfFileReader

PDFS_SIN_FOLIAR = "pdfs-sin-foliar"
PDFS_PROCESADOS = "pdfs-procesados"
PDFS_FOLIADOS = "pdfs-foliados"
PDFS_TEMPORAL = "__tmp.pdf"
TXT_HISTORIAL = "historial.txt"
TXT_FOLIADO = "foliado.txt"

def secuencia_obtiene():
    """
        Obtiene la secuencia almancenada en el archivo `foliado.txt`,
        devuelve un par ordenado: (clase,secuencia).
    """
    clase_docs = "Ninguno"
    secuencia = 1    
    try:
        file1 = open(TXT_FOLIADO,"r") 
        texto = file1.readline()
    except:
        texto = f"{clase_docs} {secuencia}"
        print(f"Archivo {TXT_FOLIADO} no encontrado o con contenido inválido")
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
        with open(TXT_FOLIADO, 'w') as file1:
            file1.write(f"{clase_docs} - {secuencia}")
            print(f"Siguiente sello: {clase_docs} - {secuencia}")
    except:
        print(f"Archivo {TXT_FOLIADO} no encontrado o con contenido inválido")


def historial_de_procesado_agrega(secuencia,nombrearchivo):
    """
        Agrega al historial el archivo de procesados.
    """
    try:
        with open(TXT_HISTORIAL, 'a') as file1:
            file1.write(str(secuencia)+" "+nombrearchivo+"\n")
    except:
        print(f"Archivo {TXT_HISTORIAL} no encontrado o con contenido inválido")


def pdf_lista_archivos_ordenados(orden):
    """
        Obtiene los archivos PDF a procesar con el orden indicado. Devuelve una lista de nombres.
        - orden: por_fecha, por_nombre (valor por defecto)
    """
    from pathlib import Path
    lista_archivos=[]

    if not os.path.isdir(f"{PDFS_SIN_FOLIAR}/"):
        os.mkdir(f"{PDFS_SIN_FOLIAR}/")
        print(f"Se generó la carpeta '{PDFS_SIN_FOLIAR}' para que ahí incorpore los archivos sin foliar")
        return lista_archivos

    if orden=="por_fecha":
        from datetime import datetime
        files = sorted(Path().rglob(f"{PDFS_SIN_FOLIAR}/*.pdf"), key=os.path.getmtime)
        if len(files)>0:
            lista_archivos=[file.name for file in files]
            print(f"{len(lista_archivos)} archivos PDF ordenados por fecha de modificación:")
            primero,ultimo=files[0],files[-1]
            print(f"Primer archivo: {datetime.fromtimestamp(os.path.getmtime(primero))} {primero.name}")
            print(f"Último archivo: {datetime.fromtimestamp(os.path.getmtime(ultimo))} {ultimo.name}\n")
    else:
        files = sorted(Path().rglob(f"{PDFS_SIN_FOLIAR}/*.pdf"), key=lambda x: x.name.lower())
        if len(files)>0:
            lista_archivos=[file.name for file in files]
            print(f"{len(lista_archivos)} archivos PDF ordenados por nombre")
            primero,ultimo=files[0],files[-1]
            print(f"Primer archivo: {primero.name}")
            print(f"Último archivo: {ultimo.name}\n")    
    return lista_archivos


def pdf_imprime_sellos(num, tmp, clase_docs, secuencia):
    """
        Imprime los sellos con la secuencia en hojas limpias, usa archivo temporal.
    """
    lienzo = canvas.Canvas(tmp)
    for i in range(0,num): 
        lienzo.setFont("Helvetica", 20)
        lienzo.setFillColorRGB(0, 0, 0.77)
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
    if not os.path.isdir(f"{PDFS_PROCESADOS}/"):
        os.mkdir(f"{PDFS_PROCESADOS}/")
    path1 = os.path.join(PDFS_SIN_FOLIAR, nombre)
    path2 = os.path.join(PDFS_PROCESADOS, nombre)
    move(path1, path2)


if __name__ == "__main__":
    print("\nHerramienta foliadora de archivos en formato PDF.\n")
    argv = sys.argv
    continuar = True
    ordenamiento = "por_nombre"
    solo_orden = "solo_orden" in argv
    consultar = not "no_consultar" in argv
    if "ayuda" in argv or "help" in argv:
        print(__doc__)
        exit()
    if "por_fecha" in argv:
        ordenamiento = "por_fecha"

    (clase_docs,secuencia) = secuencia_obtiene()
    lista_archivos_pdf = pdf_lista_archivos_ordenados(ordenamiento)

    if len(lista_archivos_pdf)==0:
        print("Sin archivos para foliar")
        exit()
    if solo_orden:
        exit()

    if consultar:
        captura = input("\nIngrese la palabra 'salir' para salir, otro ingreso o solo enter continuará con el proceso: ")
    continuar = captura.lower() != "salir"
    if not continuar:
        print("\nFin del proceso")
        exit()

    print("\n")

    output = PdfFileWriter()
    for filename in lista_archivos_pdf:
        base = os.path.basename(filename)
        path = os.path.join(PDFS_SIN_FOLIAR, filename)
        if os.path.isdir(path):
            # saltar directorios
            continue
        if filename.endswith('.pdf'):
            with open(path, "rb") as f:
                print(f"Inicia con archivo {filename}")
                historial_de_procesado_agrega(secuencia, filename)
                pdf = PdfFileReader(f, strict=False)
                n = pdf.getNumPages()
                pdf_imprime_sellos(n, PDFS_TEMPORAL, clase_docs, secuencia)
                secuencia=secuencia+n

                if not os.path.isdir(f"{PDFS_FOLIADOS}/"):
                    os.mkdir(f"{PDFS_FOLIADOS}/")
                with open(PDFS_TEMPORAL, "rb") as ftmp:
                    numberPdf = PdfFileReader(ftmp)
                    newpath = f"{PDFS_FOLIADOS}/"+ base
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
                        newpath = f"{PDFS_FOLIADOS}/" + base
                        with open(newpath, "wb") as f:
                            output.write(f)            
                os.remove(PDFS_TEMPORAL)
            pdf_mueve(filename)
            print(f"Termina con archivo {filename}\n")

    if len(lista_archivos_pdf)>0:
        secuencia_actualiza(clase_docs, secuencia)        
        print("\nFin del proceso")
    else:
        print("\nNo hubo archivos para foliar")
