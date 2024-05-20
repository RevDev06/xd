from flask import Flask, render_template
import pymysql

#forma pdf-python
import os
import webbrowser
from fpdf import FPDF

app = Flask(__name__)

@app.route('/')
def home():
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rh3')
    cursor = conn.cursor()
    cursor.execute('select c.idCandidato, c.nombre, p.nomPuesto from candidato c, puesto p where c.idPuesto = p.idPuesto')
    datos = cursor.fetchall()
    return render_template("index.html", comentarios = datos,)

@app.route('/index')
def inicio():
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rh3')
    cursor = conn.cursor()
    cursor.execute('select c.idCandidato, c.nombre, p.nomPuesto from candidato c, puesto p where c.idPuesto = p.idPuesto')
    datos = cursor.fetchall()
    return render_template("index.html", comentarios = datos, )


@app.route('/cont_j/<string:idC>', methods=['GET'])
def contrato_j(idC):
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rh3')
    cursor = conn.cursor()

    cursor.execute('select p.idPuesto from puesto p, candidato c where p.idPuesto = c.idPuesto and c.idCandidato = %s', (idC))
    idP = cursor.fetchall()

    cursor.execute('select nombre, edad, sexo, CURP, RFC, domCalle, domNumExtInt, domColonia, correoE, tel1, tel2 '
            'from candidato where idCandidato = %s', (idC))
    datos = cursor.fetchall()

    cursor.execute('select puestoJefeSup, nomPuesto, codPuesto, jornada, remunMensual, prestaciones, descripcionGeneral,'
            'funciones, experiencia, conocimientos, manejoEquipo, reqFisicos, reqPsicologicos, condicionesTrabajo, responsabilidades ' 
            'from puesto where idPuesto = %s', (idP))
    dato = cursor.fetchall()

    cursor.execute('select a.idArea, a.descripcion from area a, puesto b where a.idArea = b.idArea and b.idPuesto = %s', (idP))
    datos1 = cursor.fetchall()

    cursor.execute('select a.idEstadoCivil, a.descripcion from estado_civil a, candidato b where a.idEstadoCivil = b.idEstadoCivil and b.idCandidato = %s', (idC))
    datos2 = cursor.fetchall()

    cursor.execute('select a.idEscolaridad, a.descripcion from escolaridad a, candidato b where a.idEscolaridad = b.idEscolaridad and b.idCandidato = %s', (idC))
    datos3 = cursor.fetchall()

    cursor.execute('select a.idGradoAvance, a.descripcion from grado_avance a, candidato b where a.idGradoAvance = b.idGradoAvance and b.idCandidato = %s', (idC))
    datos4 = cursor.fetchall()

    cursor.execute('select a.idCarrera, a.descripcion from carrera a, candidato b where a.idCarrera = b.idCarrera and b.idCandidato = %s', (idC))
    datos5 = cursor.fetchall()

    cursor.execute('select a.idPuesto, b.idIdioma, b.descripcion from puesto a, idioma b, puesto_has_idioma c '
                   'where a.idPuesto = c.idPuesto and b.idIdioma = c.idIdioma and a.idPuesto = %s', (idP))
    datos6 = cursor.fetchall()

    cursor.execute('select a.idPuesto, b.idHabilidad, b.descripcion from puesto a, habilidad b, puesto_has_habilidad c '
                   'where a.idPuesto = c.idPuesto and b.idHabilidad = c.idHabilidad and a.idPuesto = %s', (idP))
    datos7 = cursor.fetchall()

    cursor.execute('select p.nomPuesto, a.descripcion, p.puestoJefeSup, p.jornada, p.funciones, p.responsabilidades, p.remunMensual,' 
                   'p.prestaciones from puesto p, area a where a.idArea = p.idArea and idPuesto = %s', (idP))
    clausu1 = cursor.fetchall()

    cursor.execute('select r.fechainicVac, c.nombre, p.nomPuesto from puesto p, requisicion r, candidato c where r.idRequisicion = c.idRequisicion and ' 
                   'p.idPuesto = c.idPuesto and c.idCandidato = %s', (idC))
    clausu2 = cursor.fetchall()

    return render_template("contrato.html", llenar = datos, tablap=dato, catArea=datos1, catEdoCivil=datos2, catEscolaridad=datos3,
                           catGradoAvance=datos4, catCarrera=datos5, catIdioma=datos6, catHabilidad=datos7, claus1 = clausu1, claus2 = clausu2)



#opcion 2(mas factible):
#Tengo que obtener el id de el puesto y del candidato para poder ir llenando todos los datos
"""@app.route('/cont_p/<string:idP>', methods=['GET<']')
def contrato_p():
    conn = pymysql.connect(host='localhost', user='root', passwd='', db='rh3')
    cursor = conn.cursor()
    cursor.execute('select c.nombre, c.CURP, c.RFC, c.domCalle, c.domNumExtInt, c.domColonia, c.tel1, c.tel2, c.correoE from candidato c, puesto p where c.idPuesto = p.idPuesto,')
    datos = cursor.fetchall()
    cursor.execute('select idArea, descripcion from area order by idArea')
    datos = cursor.fetchall()
    return render_template("area.html", comentarios = datos, )"""

if __name__ == "__main__":
    app.run(debug=True)