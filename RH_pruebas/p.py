import os
import pymysql
from fpdf import FPDF
import webbrowser

conn = pymysql.connect(host='localhost', user='root', passwd='', db='tf1')
cursor = conn.cursor()
cursor.execute('select id, nombre, apellido, usuario from contacto order by id')
datos = cursor.fetchall()
# Crear un objeto FPDF con orientación vertical, unidades en milímetros y formato A4
pdf = FPDF(orientation='P', unit='mm', format='A4')

# Agregar una nueva página al PDF
pdf.add_page()

# Establecer la fuente. Esto es necesario antes de agregar cualquier texto.
pdf.set_font('Arial', 'B', 16)

# Agregar contenido de ejemplo al PDF
pdf.cell(40, 10, 'Hello World!')
pdf.ln(10)


# Establecer la fuente
pdf.set_font('Arial', 'B', 12)

# Agregar el encabezado de la tabla
pdf.cell(10, 10, 'ID', 1)
pdf.cell(40, 10, 'Name', 1)
pdf.cell(20, 10, 'Age', 1)
pdf.cell(80, 10, 'Email', 1)
pdf.ln()

# Agregar los datos de la base de datos
pdf.set_font('Arial', '', 12)
for row in datos:
    pdf.cell(10, 10, str(row[0]), 1)
    pdf.cell(40, 10, row[1], 1)
    pdf.cell(20, 10, str(row[2]), 1)
    pdf.cell(80, 10, row[3], 1)
    pdf.ln()

pdf.set_font('Arial', '', 12)
for row in datos:
    pdf.cell(0, 10, f'ID: {row[0]}', 0, 1)
    pdf.cell(0, 10, f'Name: {row[1]}', 0, 1)
    pdf.cell(0, 10, f'Age: {row[2]}', 0, 1)
    pdf.cell(0, 10, f'Email: {row[3]}', 0, 1)
    pdf.ln()


# Especificar una ruta absoluta para guardar el archivo PDF
archivo = "Contrato laboral de "+row[1]+".pdf"
output_path = os.path.join(os.path.expanduser('~'), 'Desktop', archivo)
webbrowser.open(output_path)
pdf.output(output_path)

print(f'Nombre:{archivo}')
print(f'Archivo PDF guardado en {output_path}')
conn.close()