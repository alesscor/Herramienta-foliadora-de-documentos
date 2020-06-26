import reportlab
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from PyPDF2 import PdfFileWriter, PdfFileReader

def obtiene_secuencia():
    return "Enviados - 2038"

def modifica_pdf(num, tmp, clase_docs, secuencia):
    c = canvas.Canvas(tmp)
    for i in range(0,num): 
        c.rotate(90)
        c.setFillColorRGB(0,0,0.77)
        c.drawString((5)*mm, (-5)*mm, clase_docs + " - " + str(i+secuencia))
        c.showPage()
    c.save()
    return

if __name__ == "__main__":
    import sys, os
    tmp = "__tmp.pdf"
    
    output = PdfFileWriter()

    clase_docs=obtiene_secuencia()
    secuencia=int(clase_docs.split(" - ")[1])
    clase_docs=clase_docs.split(" - ")[0]

    for filename in os.listdir("Herramienta foliadora de documentos/pdfs-sin-foliar"):
        base = os.path.basename(filename)
        path = os.path.join('Herramienta foliadora de documentos/pdfs-sin-foliar', filename)
        if filename.endswith('.pdf'):            
            with open(path, "rb") as f:
                pdf = PdfFileReader(f,strict=False)
                n = pdf.getNumPages()
                modifica_pdf(n,tmp,clase_docs,secuencia)
                secuencia=secuencia+n

                if not os.path.isdir("Herramienta foliadora de documentos/pdfs-foliados/"):
                    os.mkdir("Herramienta foliadora de documentos/pdfs-foliados/")
                with open(tmp, "rb") as ftmp:
                    numberPdf = PdfFileReader(ftmp)
                    newpath = "Herramienta foliadora de documentos/pdfs-foliados/"+ base
                    with open(newpath, "wb") as f:
                        output.write(f)
                    output = PdfFileWriter()
                    for p in range(n):                                                    
                        # sys.stdout.write("\rpage: %d of %d"%(p, n))
                        print("page: %d of %d"%(p, n))
                        page = pdf.getPage(p)
                        numberLayer = numberPdf.getPage(p)
                        
                        page.mergePage(numberLayer)
                        output.addPage(page)
                    if output.getNumPages():
                        newpath = "Herramienta foliadora de documentos/pdfs-foliados/" + base
                        with open(newpath, "wb") as f:
                            output.write(f)            
                os.remove(tmp)