from flask import Flask, render_template, request, redirect, send_file, url_for, flash
import pymysql
import os
from fpdf import FPDF
import mimetypes
from email.message import EmailMessage
import ssl
import smtplib

class EmailSender:
    def __init__(self, sender_email, sender_password, smtp_server='smtp.gmail.com', smtp_port=465):
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
    
    def send_email(self, recipient_email, subject, body, attachments=None):
        email_message = EmailMessage()
        email_message['From'] = self.sender_email
        email_message['To'] = recipient_email
        email_message['Subject'] = subject
        email_message.set_content(body)

        if attachments:
            for file_path in attachments:
                mime_type, _ = mimetypes.guess_type(file_path)
                if mime_type is None:
                    mime_type = 'application/octet-stream'
                mime_type, mime_subtype = mime_type.split('/')

                with open(file_path, 'rb') as file:
                    email_message.add_attachment(file.read(),
                                                maintype=mime_type,
                                                subtype=mime_subtype,
                                                filename=file_path.split('/')[-1])
        
        context = ssl.create_default_context()
        
        with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context) as smtp:
            smtp.login(self.sender_email, self.sender_password)
            smtp.sendmail(self.sender_email, recipient_email, email_message.as_string())

app = Flask(__name__)

@app.route('/')
def home():
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rh3')
    cursor = conn.cursor()
    cursor.execute('select c.idCandidato, c.nombre, p.nomPuesto from candidato c, puesto p where c.idPuesto = p.idPuesto')
    datos = cursor.fetchall()
    return render_template("index.html", comentarios=datos)

@app.route('/index')
def inicio():
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rh3')
    cursor = conn.cursor()
    cursor.execute('select c.idCandidato, c.nombre, p.nomPuesto from candidato c, puesto p where c.idPuesto = p.idPuesto')
    datos = cursor.fetchall()
    
    return render_template("index.html", comentarios=datos)

@app.route('/cont_p/<string:idC>', methods=['GET'])
def contrato_p(idC):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rh3')
    cursor = conn.cursor()

    cursor.execute('select p.idPuesto from puesto p, candidato c where p.idPuesto = c.idPuesto and c.idCandidato = %s', (idC,))
    idP = cursor.fetchone()

    cursor.execute('select c.idCandidato, c.nombre, p.nomPuesto from candidato c, puesto p where c.idPuesto = p.idPuesto')
    r = cursor.fetchall()

    cursor.execute('select nombre, edad, sexo, CURP, RFC, domCalle, domNumExtInt, domColonia, correoE, tel1, tel2 from candidato where idCandidato = %s', (idC,))
    datos = cursor.fetchone()

    cursor.execute('select puestoJefeSup, nomPuesto, codPuesto, jornada, remunMensual, prestaciones, descripcionGeneral, funciones, experiencia, conocimientos, manejoEquipo, reqFisicos, reqPsicologicos, condicionesTrabajo, responsabilidades from puesto where idPuesto = %s', (idP,))
    dato = cursor.fetchone()

    cursor.execute('select a.idArea, a.descripcion from area a, puesto b where a.idArea = b.idArea and b.idPuesto = %s', (idP,))
    datos1 = cursor.fetchone()

    cursor.execute('select a.idEstadoCivil, a.descripcion from estado_civil a, candidato b where a.idEstadoCivil = b.idEstadoCivil and b.idCandidato = %s', (idC,))
    datos2 = cursor.fetchone()

    cursor.execute('select a.idEscolaridad, a.descripcion from escolaridad a, candidato b where a.idEscolaridad = b.idEscolaridad and b.idCandidato = %s', (idC,))
    datos3 = cursor.fetchone()

    cursor.execute('select a.idGradoAvance, a.descripcion from grado_avance a, candidato b where a.idGradoAvance = b.idGradoAvance and b.idCandidato = %s', (idC,))
    datos4 = cursor.fetchone()

    cursor.execute('select a.idCarrera, a.descripcion from carrera a, candidato b where a.idCarrera = b.idCarrera and b.idCandidato = %s', (idC,))
    datos5 = cursor.fetchone()

    cursor.execute('select a.idPuesto, b.idIdioma, b.descripcion from puesto a, idioma b, puesto_has_idioma c where a.idPuesto = c.idPuesto and b.idIdioma = c.idIdioma and a.idPuesto = %s', (idP,))
    datos6 = cursor.fetchone()

    cursor.execute('select a.idPuesto, b.idHabilidad, b.descripcion from puesto a, habilidad b, puesto_has_habilidad c where a.idPuesto = c.idPuesto and b.idHabilidad = c.idHabilidad and a.idPuesto = %s', (idP,))
    datos7 = cursor.fetchone()

    cursor.execute('select p.nomPuesto, a.descripcion, p.puestoJefeSup, p.jornada, p.funciones, p.responsabilidades, p.remunMensual, p.prestaciones from puesto p, area a where a.idArea = p.idArea and idPuesto = %s', (idP,))
    clausu1 = cursor.fetchone()

    cursor.execute('select r.fechainicVac, c.nombre, p.nomPuesto from puesto p, requisicion r, candidato c where r.idRequisicion = c.idRequisicion and p.idPuesto = c.idPuesto and c.idCandidato = %s', (idC,))
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
        f'Condiciones de trabajo: {dato[13]}',
        f'Responsabilidades: {dato[14]}'
    ]
    for item in puesto:
        pdf.chapter_datos(item)

    # Add a line break
    pdf.ln(10)

    # Add the candidate section
    pdf.chapter_title('DATOS DEL CANDIDATO')
    candidato = [
        f'Nombre: {datos[0]}',
        f'Edad: {datos[1]}',
        f'Sexo: {datos[2]}',
        f'Estado civil: {datos2[1]}',
        f'CURP: {datos[3]}',
        f'RFC: {datos[4]}',
        f'Direccion: {datos[5]} {datos[6]}, {datos[7]}',
        f'Correo electronico: {datos[8]}',
        f'Telefono 1: {datos[9]}',
        f'Telefono 2: {datos[10]}',
        f'Escolaridad: {datos3[1]}',
        f'Grado avance: {datos4[1]}',
        f'Carrera: {datos5[1]}',
        f'Idioma: {datos6[2]}',
        f'Habilidad: {datos7[2]}'
    ]
    for item in candidato:
        pdf.chapter_datos(item)

    # Add a line break
    pdf.ln(10)

    # Add the clauses section
    pdf.chapter_title('CLAUSULAS')
    clausulas = [
        f'Nombre: {clausu1[1]}',
        f'Puesto: {clausu1[0]}',
        f'Jornada: {clausu1[3]}',
        f'Funciones: {clausu1[4]}',
        f'Responsabilidades: {clausu1[5]}',
        f'Remuneracion mensual: {clausu1[6]}',
        f'Prestaciones: {clausu1[7]}',
        f'Fecha de inicio: {clausu2[0]}',
        'Días de vacaciones: 3 dias',
        f'Nombre del candidato: {clausu2[1]}',
        f'Puesto del candidato: {clausu2[2]}'
    ]
    for item in clausulas:
        pdf.chapter_datos(item)

    # Define the path for the temporary PDF file
    pdf_path = 'RH_pruebas/static/Contrato.pdf'
    # Output the PDF to the defined path
    pdf.output(pdf_path)

    return redirect(url_for('send_email', pdf_path=pdf_path))

@app.route('/send_email')
def send_email():
    pdf_path = request.args.get('pdf_path')
    sender_email = 'pruebaautomatizacionemails@gmail.com'
    sender_password = 'hquw jsca rrym lwas'
    recipient_email = '22301061550002@cetis155.edu.mx'
    subject = 'Contrato Laboral'
    body = 'Adjunto encontrarás el contrato laboral en formato PDF.'

    email_sender = EmailSender(sender_email, sender_password)
    email_sender.send_email(recipient_email, subject, body, [pdf_path])


    flash('Correo enviado correctamente')
    return redirect(url_for('inicio'))

if __name__ == '__main__':
    app.secret_key = 'mysecretkey'
    app.run(port=5000, debug=True)
