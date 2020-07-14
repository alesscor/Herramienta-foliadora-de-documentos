# Introducción 
Herramienta para escribir secuencia de control en archivos de formato PDF.

Usa la técnica de generar las páginas en blanco con el sello de control, para luego imprimirlo en el documento con el contenido, dejándolo en carpeta `pdfs-foliados`.

## Versión original
- Tomado del trabajo de Lei Yang (https://gist.github.com/DIYer22/b9ede6b5b96109788a47973649645c1f), usando componentes de `reportlab`.

## Componentes principales
- Biblioteca `reportlab`, licencia [BSD](https://en.wikipedia.org/wiki/BSD_licenses). Descripción en (https://pypi.org/project/reportlab/).
- Biblioteca `PyPDF2`, licencia [BSD](https://en.wikipedia.org/wiki/BSD_licenses). Descripción en (https://pypi.org/project/PyPDF2/)
- Para una posible versión gráfica se piensa utilizar `wxPython`, licencia [wxWindows](https://opensource.org/licenses/wxwindows.php) (parecido a GPL con modificación).
- Por ahora el usuario no ha solicitado versión gráfica, en ambiente Windows 10 ha bastado con la simple interfaz de archivos `.bat` incluyendo `PAUSE` para ver resultados.

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

