
import pymysql
import os
import webbrowser
from fpdf import FPDF

idC=1
conn = pymysql.connect(host='localhost', user='root', passwd='', db='rh3')
cursor = conn.cursor()
cursor.execute('select p.idPuesto from puesto p, candidato c where p.idPuesto = c.idPuesto and c.idCandidato = %s', (idC))
idP = cursor.fetchone()

cursor.execute('select nombre, edad, sexo, CURP, RFC, domCalle, domNumExtInt, domColonia, correoE, tel1, tel2 '
        'from candidato where idCandidato = %s', (idC))
datos = cursor.fetchone()

cursor.execute('select puestoJefeSup, nomPuesto, codPuesto, jornada, remunMensual, prestaciones, descripcionGeneral, funciones, experiencia, '
               'conocimientos, manejoEquipo, reqFisicos, reqPsicologicos, condicionesTrabajo, responsabilidades from puesto where idPuesto = %s', (idP,))
dato = cursor.fetchone()

cursor.execute('select a.idArea, a.descripcion from area a, puesto b where a.idArea = b.idArea and b.idPuesto = %s', (idP))
datos1 = cursor.fetchone()

cursor.execute('select a.idEstadoCivil, a.descripcion from estado_civil a, candidato b where a.idEstadoCivil = b.idEstadoCivil and b.idCandidato = %s', (idC))
datos2 = cursor.fetchone()

cursor.execute('select a.idEscolaridad, a.descripcion from escolaridad a, candidato b where a.idEscolaridad = b.idEscolaridad and b.idCandidato = %s', (idC))
datos3 = cursor.fetchone()

cursor.execute('select a.idGradoAvance, a.descripcion from grado_avance a, candidato b where a.idGradoAvance = b.idGradoAvance and b.idCandidato = %s', (idC))
datos4 = cursor.fetchone()

cursor.execute('select a.idCarrera, a.descripcion from carrera a, candidato b where a.idCarrera = b.idCarrera and b.idCandidato = %s', (idC))
datos5 = cursor.fetchone()

cursor.execute('select a.idPuesto, b.idIdioma, b.descripcion from puesto a, idioma b, puesto_has_idioma c '
                'where a.idPuesto = c.idPuesto and b.idIdioma = c.idIdioma and a.idPuesto = %s', (idP))
datos6 = cursor.fetchone()

cursor.execute('select a.idPuesto, b.idHabilidad, b.descripcion from puesto a, habilidad b, puesto_has_habilidad c '
                'where a.idPuesto = c.idPuesto and b.idHabilidad = c.idHabilidad and a.idPuesto = %s', (idP))
datos7 = cursor.fetchone()

cursor.execute('select p.nomPuesto, a.descripcion, p.puestoJefeSup, p.jornada, p.funciones, p.responsabilidades, p.remunMensual,' 
                'p.prestaciones from puesto p, area a where a.idArea = p.idArea and idPuesto = %s', (idP))
clausu1 = cursor.fetchone()

cursor.execute('select r.fechainicVac, c.nombre, p.nomPuesto from puesto p, requisicion r, candidato c where r.idRequisicion = c.idRequisicion and ' 
                'p.idPuesto = c.idPuesto and c.idCandidato = %s', (idC))
clausu2 = cursor.fetchone()

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 15, 'CONTRATO LABORAL', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(5)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 7, body)
        self.ln()

    def chapter_datos(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 3, body)
        self.ln()

# Create instance of FPDF class
pdf = PDF()

# Add a page
pdf.add_page()

# Set title
pdf.set_font('Arial', 'B', 16)

# Add the company section
pdf.chapter_title('DATOS DE LA EMPRESA')
empresa = [
    'Nombre: Swift Market',
    'Ubicacion: Av. Perseo 301, Ptimo Verdad Inegi',
    'Codigo Postal: 20267',
    'Municipio: Aguascalientes',
    'Estado: Aguascalientes',
    'Detalles: Se dedica a la venta de productos'
]
for item in empresa:
    pdf.chapter_datos(item)

# Add a line break
pdf.ln(10)

# Add the job section
pdf.chapter_title('DATOS DEL PUESTO')
puesto = [
    f'Supervisor: {dato[0]}',
    f'Nombre del puesto: {dato[1]}',
    f'Código del puesto: {dato[2]}',
    f'Area: {datos1[1]}',
    f'Jornada: {dato[3]}',
    f'Remuneracion mensual: {dato[4]}',
    f'Prestaciones: {dato[5]}',
    'Fecha de pago: 30 de cada mes',
    'Forma de pago: Efectivo',
    f'Descripcion general: {dato[6]}',
    'Estancia: 3 meses',
    'Vacaciones: No',
    'Lugar de trabajo: Empresa',
    'Duración de contrato: 3 meses',
    f'Funciones: {dato[7]}',
    f'Experiencia: {dato[8]}',
    f'Conocimientos: {dato[9]}',
    f'Manejo de equipo: {dato[10]}',
    f'Requisitos fisicos: {dato[11]}',
    f'Requisitos psicologicos: {dato[12]}',
    f'Idiomas: {datos6[2]}',
    f'habilidades: {datos7[2]}',
    f'Condiciones de trabajo: {dato[13]}',
    f'Responsabilidades: {dato[14]}'
]
for item in puesto:
    pdf.chapter_datos(item)

# Add a line break
pdf.ln(10)

# Add the worker section
pdf.chapter_title('DATOS DEL TRABAJADOR')
trabajador = [
    f'Nombre: {datos[0]}',
    f'Edad: {datos[1]}',
    f'Sexo: {datos[2]}',
    f'CURP: {datos[3]}',
    f'RFC: {datos[4]}',
    f'Domicilio: {datos[5]} {datos[6]} {datos[7]}',
    f'Correo electronico: {datos[8]}',
    f'Telefono 1: {datos[9]}',
    f'Telefono 2: {datos[10]}',
    f'Estado civil: {datos2[1]}',
    f'Escolaridad: {datos3[1]}',
    f'Grado de avance: {datos4[1]}',
    f'Carrera: {datos5[1]}'
]
for item in trabajador:
    pdf.chapter_datos(item)

# Add a line break
pdf.ln(10)

# Add clauses section
pdf.chapter_title('CLÁUSULAS')
clausulas = [
    f'1. Al firmar esta dispuesto a trabajar en la empresa "Swift Market" ubicada en Av. Perseo 301, Ptimo Verdad Inegi, en el puesto de {clausu1[0]} en el area de Area Name a cargo del {clausu1[1]}, durante la jornada de {clausu1[2]}, en la cual va a tener que {clausu1[3]} y sus responsabilidades seran {clausu1[4]}, al hacer esto se le dara un pago de {clausu1[5]} al mes, con prestaciones {clausu1[7]}.',
    f'2. Citando la Ley Federal de Trabajo Articulo 38-39 se establece que la empresa se compromete a cumplir con la capacitacion inicial desde el dia {clausu2[0]} del candidato {clausu2[1]} para el puesto {clausu2[2]}, capacitando y adiestrando todas sus funciones y responsabilidades que son requeridas para el puesto de forma segura y saludable para ambas partes del contrato.',
    '3. La empresa se compromete a darle todo el equipo, conocimientos y ambiente que necesita a el trabajador para realizar su trabajo en la empresa. Las lecciones de la capacitacion se dara dentro de la empresa con su respectivo supervisor en el horario de la jornada.',
    '4. La trabajador se debe comprometer a asistir a todas las lecciones de su capacitacion, participar activamente y lleavr a cabo todo lo aprendido de estas en su laboral.',
    '5. En caso de cualquier conflicto que suceda entre empleados ya sea fuera o dentro de la empresa tendra que ser informado a recursos humanos para poder llegar a la causa del problema y a una solucion para la sana convivencia en el area de trabajo y en el horario de trabajo. En caso de que el problema sea muy grave se tomaran medidas con el trabajador y su contrato puede terminar antes.',
    '6. Cualquier cosa echa dentro de la empresa que no este relacionada a su trabajo le pertenecera a la misma empresa.',
    '7. Mientras trabaje en la empresa no podra hacer ningun trabajo ya sea externo o propio el cual sea competencia con la empresa.',
    '8. Al finalizar el contrato, su supervisor se encargara de dar un imforme del progreso y rendimiento en el periodo que estuvo en la empresa y se decidira si se le ofrece un nuevo contrato.',
    '9. Despues de firmar ambas partes esta aceptando tener alta confidencialidad sobre la empresa y lo que pase dentro de la misma incluyendo datos o estadisticas de los ingresos de la empresa.'
]
for item in clausulas:
    pdf.chapter_body(item)

# Add signatures section
pdf.ln(20)
pdf.cell(90, 10, '_____________________')
pdf.cell(90, 10, '_____________________')
pdf.ln(10)
pdf.cell(90, 10, 'Firma del supervisor')
pdf.cell(90, 10, 'Firma del trabajador')

# Output the PDF
# Especificar una ruta absoluta para guardar el archivo PDF
archivo = "Contrato laboral.pdf"
output_path = os.path.join(os.path.expanduser('~'), 'Desktop', archivo)
webbrowser.open(output_path)
pdf.output(output_path)
print(f'Nombre:{archivo}')
print(f'Archivo PDF guardado en {output_path}')
