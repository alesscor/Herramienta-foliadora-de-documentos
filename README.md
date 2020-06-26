# Introducción 
Herramienta para escribir secuencia de control en archivos de formato PDF.

Usa la filosofía de generar las páginas en blanco con el sello de control, para luego imprimirlo en el documento con el contenido, dejándolo en carpeta `pdfs-foliados`.

## Versión original
- Tomado del trabajo de Lei Yang (https://gist.github.com/DIYer22/b9ede6b5b96109788a47973649645c1f), usando componentes de `reportlab`.

## Componentes principales
- Biblioteca `reportlab`, licencia [BSD](https://en.wikipedia.org/wiki/BSD_licenses). Descripción en (https://pypi.org/project/reportlab/).
- Biblioteca `PyPDF2`, licencia [BSD](https://en.wikipedia.org/wiki/BSD_licenses). Descripción en (https://pypi.org/project/PyPDF2/)
- Para la versión gráfica se piensa utilizar `wxPython`, licencia [wxWindows](https://opensource.org/licenses/wxwindows.php) (parecido a GPL con modificación).
