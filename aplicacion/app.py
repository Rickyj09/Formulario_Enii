from http.client import OK
from pydoc import html
from typing import Text
from flask import Flask, render_template, request, redirect, url_for, flash, make_response
from flask_sqlalchemy import SQLAlchemy
from aplicacion import config
from aplicacion.forms import datos_equipo, datos_reporte, check_list2, check_list3, FormArticulo
from aplicacion.forms import check_list4, check_list5, check_list6, check_list7, check_list8, check_list9
from aplicacion.forms import check_list10, check_list11, check_list12, check_list13, check_list14, check_list15
from aplicacion.forms import check_list16, check_list17, check_list18, check_list19, check_list20, check_list21
from aplicacion.forms import check_list22, check_list23, check_list24, check_list25, buscaform, CHECK_LIST_FIN
from aplicacion.forms import prueba_carga, check_list1, prueba_carga3,list_formulario
from aplicacion.forms import formu1, formu1_1, formu2, formu3, formu4, formu5, formu6, formu7, formu8, formu9, formu10, formu11, formu12, formu13
from aplicacion.forms import formu2_2, formu3_3, formu4_4, formu5_5, formu6_6,formu12_1,formu13_1
from aplicacion.forms import LoginForm, UploadForm
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
from flask_wtf.file import FileField, FileRequired
from wtforms.fields.html5 import DateField
from jinja2 import Environment, FileSystemLoader
from os import listdir
from flask_login import LoginManager, login_user, logout_user, login_required,\
    current_user
from aplicacion.forms import LoginForm, FormUsuario
import pdfkit
import os

import xhtml2pdf.pisa as pisa
from io import StringIO
#from flask_weasyprint import HTML, render_pdf



UPLOAD_FOLDER = os.path.abspath("./static/uploads/")
ALLOWED_EXTENSIONS = set(["png", "jpg", "jpge"])


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


app = Flask(__name__)
app.config.from_object(config)

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# Mysql Connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'test_1'
mysql = MySQL(app)

# setting
app.secret_key = 'millave'


@login_manager.user_loader
def load_user(user_id):
    return (user_id)


#@app.route('/genera_pdf2_test')
#@login_required
#def genera_pdf2_test():
 #  cursor.execute(
  #      "select num_rep from formulario where id_formulario = (select MAX(b.id_formulario) from formulario a inner join frpol b on a.id_formulario = b.id_formulario);")
   # num_rep = cursor.fetchone()
   # cursor.execute(
    #    "select * from frpol where id_formulario = (select MAX(b.id_formulario) from formulario a inner join frpol b on a.id_formulario = b.id_formulario);")
    #datos1 = cursor.fetchall()
    #cursor.execute(
    #    "select MAX(id) from frpol ;")
    #data1 = cursor.fetchone()
    #cursor.execute(
     #   "select * from frpol1 where id_f2 = (select MAX(id) from frpol) ;")
    #data = cursor.fetchall()
    #cursor.execute(
     #   "select * from formulario where id_formulario = (select MAX(id_formulario) from formulario) and llave_formulario='FR-INSP-041.04';")
    #for_emi = cursor.fetchall()
    #cursor.execute(
     #   "select descr from cat_form where codigo = 'FR-INSP-043.03';")
    #cata = cursor.fetchone()
    #html1 = StringIO(render_template('resum_frpol.html',num_rep=num_rep, datos1=datos1, contact=data1[0], data=data,for_emi=for_emi,cata=cata).encode("UTF-8"))
    #pdf = pisa.CreatePDF(html1,dest=resultFile)
    #resultFile = StringIO()
    #pisa.showLogging()
    #return pdf

@app.route('/')
def inicio():
    return render_template("inicio.html")


@app.route('/inicio_1')
@app.route('/inicio_1/<id>')
def inicio_1(id='0'):
    from aplicacion.models import Articulos, Categorias
    categoria = Categorias.query.get(id)
    if id == '0':
        articulos = Articulos.query.all()
    else:
        articulos = Articulos.query.filter_by(CategoriaId=id)
    categorias = Categorias.query.all()
    return render_template("inicio_1.html", articulos=articulos, categorias=categorias, categoria=categoria)


@app.route('/inicio_new')
@app.route('/inicio_new/<id>')
def inicio_new(id='0'):
    from aplicacion.models import Articulos, Categorias
    categoria = Categorias.query.get(id)
    if id == '0':
        articulos = Articulos.query.all()
    else:
        articulos = Articulos.query.filter_by(CategoriaId=id)
    categorias = Categorias.query.all()
    return render_template("inicio_new.html", articulos=articulos, categorias=categorias, categoria=categoria)


@app.route('/articulos/<id>/edit', methods=["get", "post"])
@login_required
def articulos_edit(id):
    from aplicacion.models import Articulos, Categorias
    # Control de permisos
    if not current_user.is_admin():
        return render_template("404.html")
    art = Articulos.query.get(id)
    if art is None:
        return render_template("404.html")
    form = FormArticulo(obj=art)
    categorias = [(c.id, c.nombre) for c in Categorias.query.all()[1:]]
    form.CategoriaId.choices = categorias
    if form.validate_on_submit():
        # Borramos la imagen anterior si hemos subido una nueva
        if form.photo.data:
            os.remove(app.root_path + "/static/upload/" + art.image)
            try:
                f = form.photo.data
                nombre_fichero = secure_filename(f.filename)
                f.save(app.root_path + "/static/upload/" + nombre_fichero)
            except:
                nombre_fichero = ""
        else:
            nombre_fichero = art.image
        form.populate_obj(art)
        art.image = nombre_fichero
        db.session.commit()
        return redirect(url_for("inicio"))
    return render_template("articulos_new.html", form=form)


@login_manager.user_loader
def load_user(user_id):
    from aplicacion.models import Usuarios
    return Usuarios.query.get(int(user_id))


@app.route('/upload', methods=['get', 'post'])
def upload():
    form = UploadForm()  # carga request.from y request.file
    if form.validate_on_submit():
        f = form.photo.data
        filename = secure_filename(f.filename)
        f.save(app.root_path+"/static/img/subidas/"+filename)
        return redirect(url_for('inicio_foto'))
    return render_template('upload.html', form=form)


@app.route('/upload_1', methods=['get', 'post'])
def upload_1():
    form = UploadForm()  # carga request.from y request.file
    if form.validate_on_submit():
        f = form.photo.data
        filename = secure_filename(f.filename)
        f.save(app.root_path+"/static/img/subidas/"+filename)
        return redirect(url_for('reporte_foto'))
    return render_template('upload_1.html', form=form)


@app.route('/inicio_foto')
@login_required
def inicio_foto():
    lista = []
    for file in listdir(app.root_path+"/static/img/subidas/"):
        lista.append(file)
    return render_template("inicio_foto.html", lista=lista)


@app.route('/reporte_foto')
@login_required
def reporte_foto():
    lista = []
    for file in listdir(app.root_path+"/static/img/subidas/"):
        lista.append(file)
    return render_template("reporte_foto.html", lista=lista)


@app.route('/reporte_foto1')
@login_required
def reporte_foto1():
    lista = []
    for file in listdir(app.root_path+"/static/img/subidas/"):
        lista.append(file)
    return render_template("reporte_foto1.html", lista=lista)


@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select llave_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    nom_form = cursor.fetchone()
    form = datos_reporte()
    if form.validate_on_submit():
        empre = request.form['empresa']
        fecha_insp = request.form['fec_inpec']
        fecha_emi = request.form['fec_emision']
        fecha_exp = request.form['fec_expiracion']
        lugar_ins = request.form['lugar_inpec']
        nombre_ins = request.form['nom_inspec']
        cursor = mysql.connection.cursor()
        cursor.execute(
            "select llave_formulario from formulario where id_formulario = 1;")
        cursor.execute('insert into formulario (llave_formulario,desc_formulario,fecha_inspec_formulario,fecha_emision_formulario,fecha_expiracion_formulario,lugar_ins_formulario,nom_inspe_formulario,empresa) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',
                       ('FR-INSP-003.06', 'REPORTE DE INSPECCIÓN DE GRÚAS', fecha_insp, fecha_emi, fecha_exp, lugar_ins, nombre_ins, empre))
        mysql.connection.commit()
        flash('Guardado Correctamente')
        datos = cursor.fetchone()
        print(datos)
        return redirect(url_for('caratula'))
    return render_template('home.html', form=form, datos=nom_form)


@app.route('/home_1', methods=['GET', 'POST'])
@login_required
def home_1():
    cursor = mysql.connection.cursor()
    cursor.execute("select nombre from articulos where id = 4;")
    nom_form = cursor.fetchone()
    cursor.execute("select descripcion from articulos where id = 4;")
    nom_form1 = cursor.fetchone()
    cur = mysql.connection.cursor()
    form = datos_reporte()
    if form.validate_on_submit():
        cur = mysql.connection.cursor()
        cur.execute("select (sec+1) from cod_rep where id = 13;")
        sec = cur.fetchone()
        print(sec)
        cur.execute("""
                    UPDATE cod_rep
                    SET sec = %s
                        WHERE id = 13
                """, sec)
        mysql.connection.commit()
        empre = request.form['empresa']
        cur.execute(
            "select CONCAT(prefijo,LPAD(sec, 5, '0')) from cod_rep where id_for = 2;")
        num_rep = cur.fetchone()
        fecha_insp = request.form['fec_inpec']
        fecha_emi = request.form['fec_emision']
        fecha_exp = request.form['fec_expiracion']
        lugar_ins = request.form['lugar_inpec']
        nombre_ins = request.form['nom_inspec']
        cursor = mysql.connection.cursor()
        cursor.execute('insert into formulario (llave_formulario,num_rep,desc_formulario,fecha_inspec_formulario,fecha_emision_formulario,fecha_expiracion_formulario,lugar_ins_formulario,nom_inspe_formulario,empresa,cod_form) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                       (nom_form,num_rep, nom_form1, fecha_insp, fecha_emi, fecha_exp, lugar_ins, nombre_ins, empre,'frpol'))
        mysql.connection.commit()
        flash('Guardado Correctamente')
        datos = cursor.fetchone()
        # return 'OK'
        return redirect(url_for('frpol'))
    return render_template('home_1.html', form=form, datos=nom_form, desc=nom_form1)


@app.route('/frpol', methods=['GET', 'POST'])
@login_required
def frpol():
    form = formu1()
    if form.validate_on_submit():
        revis = request.form['revis']
        nivel_il = request.form['nivel_il']
        con_sup = request.form['con_sup']
        met_insp = request.form['met_insp']
        tipo_il = request.form['tipo_il']
        check1 = request.form['check1']
        check2 = request.form['check2']
        check3 = request.form['check3']
        detalle = request.form['detalle']
        revis_p = request.form['revis_p']
        temp_ens = request.form['temp_ens']
        tipo_il_p = request.form['tipo_il_p']
        nivel_il_p = request.form['nivel_il_p']
        mater_base = request.form['mater_base']
        tipo_sec = request.form['tipo_sec']
        equipo = request.form['equipo']
        modelo = request.form['modelo']
        iden = request.form['iden']
        cur = mysql.connection.cursor()
        cur.execute(
            "select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
        llave_form = cur.fetchone()
        cur.execute(
            "select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
        fecha_form = cur.fetchone()
        cur.execute('insert into frpol (id_formulario,fec_formulario,proc,revis,nivel_il,con_sup,met_insp,tipo_il,check1,check2,check3,detalle,proc_p,revis_p,temp_ens,tipo_il_p,nivel_il_p,mater_base,tipo_sec,tipo_pen,marca_kit,tiem_pen,met_rem,marca_kit1,tiem_sec,for_rev,marca_kit2,tiem_rev,equipo,modelo,iden) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                    (llave_form, fecha_form, 'PR-INSP-006', revis, nivel_il, con_sup, met_insp, tipo_il, check1, check2, check3, detalle, 'PR-INSP-007', revis_p, temp_ens, tipo_il_p, nivel_il_p, mater_base, tipo_sec, 'II VISIBLE', 'Met-L-Chek  VP-31A', '5 minutos', 'REMOVIBLE SOLVENTE', 'Met-L-Chek   E-59A', '10 minutos', 'SOLVENTE REMOVED', 'Met-L-Chek   D-70', '10 minutos', equipo, modelo, iden))
        mysql.connection.commit()
        return redirect(url_for('frpol1'))
        # return render_template('frpol1.html', form=form)
    return render_template('frpol.html', form=form)


@app.route('/add_frpol1', methods=['POST'])
@login_required
def add_frpol1():
    form = formu1_1()
    cur = mysql.connection.cursor()
    cur.execute("select (sec+1) from codigo where id_for = 2;")
    sec = cur.fetchone()
    cur.execute("""
            UPDATE codigo
            SET sec = %s
                WHERE id = 2
        """, sec)
    mysql.connection.commit()
    if form.validate_on_submit():
        cur = mysql.connection.cursor()
        ref = request.form['ref']
        cur.execute(
            "select CONCAT(preffijo,LPAD(sec, 5, '0')) from codigo where id_for = 2;")
        cod_enii = cur.fetchone()
        ancho = request.form['ancho']
        diam = request.form['diam']
        vt = request.form['vt']
        pt = request.form['pt']
        cur.execute(
            "select id from frpol where id = (select MAX(id) from frpol) ;")
        llave_form = cur.fetchone()
        print(cod_enii)
        cur.execute('insert into frpol1 (ref,cod_enii,ancho,diam,vt,pt,id_f2) VALUES (%s,%s,%s,%s,%s,%s,%s)',
                    ( ref, cod_enii, ancho, diam, vt, pt, llave_form))
        mysql.connection.commit()
        return redirect(url_for('frpol1'))


@app.route('/frpol1', methods=['GET', 'POST'])
@login_required
def frpol1():
    form = formu1_1()
    cur = mysql.connection.cursor()
    cur.execute("select * from frpol1 where id_f2=(select MAX(id) from frpol) ;")
    data = cur.fetchall()
    return render_template('frpol1.html', form=form, data=data)


@app.route('/edit_frpol/<id>', methods=['POST', 'GET'])
@login_required
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM frpol WHERE id = %s', (id,))
    data = cur.fetchall()
    cur.close()
    return render_template('edit-frpol.html', contact=data[0])


@app.route('/update_frpol/<id>', methods=['POST'])
@login_required
def update_form2(id):
    if request.method == 'POST':
        proc = request.form['proc']
        revis = request.form['revis']
        nivel_il = request.form['nivel_il']
        con_sup = request.form['con_sup']
        met_insp = request.form['met_insp']
        tipo_il = request.form['tipo_il']
        check1 = request.form['check1']
        check2 = request.form['check2']
        check3 = request.form['check3']
        detalle = request.form['detalle']
        proc_p = request.form['proc_p']
        revis_p = request.form['revis_p']
        temp_ens = request.form['temp_ens']
        tipo_il_p = request.form['tipo_il_p']
        nivel_il_p = request.form['nivel_il_p']
        mater_base = request.form['mater_base']
        tipo_sec = request.form['tipo_sec']
        tipo_pen = request.form['tipo_pen']
        marca_kit = request.form['marca_kit']
        tiem_pen = request.form['tiem_pen']
        met_rem = request.form['met_rem']
        marca_kit1 = request.form['marca_kit1']
        tiem_sec = request.form['tiem_sec']
        for_rev = request.form['for_rev']
        marca_kit2 = request.form['marca_kit2']
        tiem_rev = request.form['tiem_rev']
        equipo = request.form['equipo']
        modelo = request.form['modelo']
        iden = request.form['iden']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE frpol
            SET proc = %s,
                revis = %s,
                nivel_il = %s,
				con_sup = %s,
                met_insp = %s,
				tipo_il = %s,
                check1 = %s,
				check2 = %s,
                check3 = %s,
				detalle = %s,
                proc_p = %s,
				revis_p = %s,
                temp_ens = %s,
				tipo_il_p = %s,
                nivel_il_p = %s,
				mater_base = %s,
                tipo_sec = %s,
				tipo_pen = %s,
                marca_kit = %s,
				tiem_pen = %s,
                met_rem = %s,
				marca_kit1 = %s,
                tiem_sec = %s,
				for_rev = %s,
                marca_kit2 = %s,
				tiem_rev = %s,
                equipo = %s,
				modelo = %s,
                iden = %s
            WHERE id = %s
        """, (proc, revis, nivel_il, con_sup, met_insp, tipo_il, check1, check2, check3, detalle, proc_p, revis_p, temp_ens, tipo_il_p, nivel_il_p, mater_base, tipo_sec, tipo_pen, marca_kit, tiem_pen, met_rem, marca_kit1, tiem_sec, for_rev, marca_kit2, tiem_rev, equipo, modelo, iden, id))
        flash('Contact Updated Successfully')
        mysql.connection.commit()
        return redirect(url_for('resum_frpol'))


@app.route('/edit-frpol1/<id>', methods=['POST', 'GET'])
@login_required
def get_frpol1(id):
    cur = mysql.connection.cursor()
    cur.execute(
        'SELECT * FROM frpol1 WHERE num = %s and id_f2=(select MAX(id) from frpol)', [id])
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-frpol1.html', contact=data[0])


@app.route('/update_frpol1/<id>', methods=['POST'])
@login_required
def update_frpol1(id):
    if request.method == 'POST':
        num = id
        ref = request.form['ref']
        cod_enii = request.form['cod_enii']
        ancho = request.form['ancho']
        diam = request.form['diam']
        vt = request.form['vt']
        pt = request.form['pt']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE frpol1
            SET num = %s,
                ref = %s,
                cod_enii = %s,
				ancho = %s,
                diam = %s,
                vt = %s,
				pt = %s
            WHERE num = %s
        """, (num, ref, cod_enii, ancho, diam, vt, pt, num))
        flash('Contact Updated Successfully')
        mysql.connection.commit()
        return redirect(url_for('frpol1'))


@app.route('/resum_frpol')
@login_required
def resum_frpol():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select num_rep from formulario where id_formulario = (select MAX(b.id_formulario) from formulario a inner join frpol b on a.id_formulario = b.id_formulario);")
    num_rep = cursor.fetchone()
    cursor.execute(
        "select * from frpol where id_formulario = (select MAX(b.id_formulario) from formulario a inner join frpol b on a.id_formulario = b.id_formulario);")
    datos1 = cursor.fetchall()
    cursor.execute(
        "select MAX(id) from frpol ;")
    data1 = cursor.fetchone()
    cursor.execute(
        "select * from frpol1 where id_f2 = (select MAX(id) from frpol) ;")
    data = cursor.fetchall()
    cursor.execute(
        "select * from formulario where id_formulario = (select MAX(id_formulario) from formulario) and llave_formulario='FR-INSP-041.04';")
    for_emi = cursor.fetchall()
    cursor.execute(
        "select descr from cat_form where codigo = 'FR-INSP-043.03';")
    cata = cursor.fetchone()
    print(data)
    return render_template('resum_frpol.html',num_rep=num_rep, datos1=datos1, contact=data1[0], data=data,for_emi=for_emi,cata=cata)


@app.route('/resum_frpol_1')
@login_required
def resum_frpol_1():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select * from frpol where id_formulario = (select MAX(id_formulario) from formulario);")
    datos1 = cursor.fetchall()
    cursor.execute(
        "select MAX(id) from frpol ;")
    data1 = cursor.fetchone()
    cursor.execute(
        "select * from frpol1 where id_f2 = (select MAX(id) from frpol) ;")
    data = cursor.fetchall()
    print(data1)
    print(data)
    return render_template('resum_frpol_1.html',datos1=datos1, contact=data1[0], data=data)


@app.route('/reporte_fotopol')
@login_required
def reporte_fotopol():
    lista = []
    for file in listdir(app.root_path+"/static/img/subidas/pol/"):
        lista.append(file)
    return render_template("reporte_fotopol.html", lista=lista)


@app.route('/upload_fpol', methods=['get', 'post'])
def upload_fpol():
    form = UploadForm()  # carga request.from y request.file
    if form.validate_on_submit():
        cursor = mysql.connection.cursor()
        cursor.execute("select CURDATE();")
        fecha_hoy = cursor.fetchone()
        f = form.photo.data
        filename = secure_filename(f.filename)
        f.save(app.root_path+"/static/img/subidas/pol/"+filename)
        cursor.execute(
            "select id from frpol where id = (select MAX(id) from frpol) ;")
        llave_form = cursor.fetchone()
        cursor.execute('insert into rep_foto_frpol (foto,fecha_foto,id_f) VALUES (%s,%s,%s)',
                    (filename,fecha_hoy,llave_form))
        mysql.connection.commit()
        return redirect(url_for('inicio_fotopol'))
    return render_template('upload_fpol.html', form=form)

@app.route('/inicio_fotopol')
@login_required
def inicio_fotopol():
    lista = []
    for file in listdir(app.root_path+"/static/img/subidas/pol"):
        lista.append(file)
    return render_template("inicio_fotopol.html", lista=lista)


@app.route('/cert_for1', methods=['GET', 'POST'])
@login_required
def cert_for1():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select * from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    for_emi = cursor.fetchall()
    cursor.execute(
        "select fecha_expiracion_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_exp = cursor.fetchone()
    cursor.execute(
        "select llave_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    llave = cursor.fetchone()
    cursor.execute(
        "select lugar_ins_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    lug = cursor.fetchone()
    cursor.execute(
        "select nom_inspe_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    ins = cursor.fetchone()
    cursor.execute(
        "select * from frpol1 where id_f2 = (select MAX(id) from frpol) ;")
    data = cursor.fetchall()

    return render_template('cert_for1.html', data=data, for_emi=for_emi, fec_exp=fec_exp, llave=llave, lug=lug, ins=ins)


@app.route('/resumen_foto_pol', methods=['GET', 'POST'])
@login_required
def resumen_foto_pol():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select num_rep from formulario where id_formulario = (select MAX(b.id_formulario) from formulario a inner join frpol b on a.id_formulario = b.id_formulario);")
    num_rep = cursor.fetchone()
    cursor.execute(
        "select * from formulario where id_formulario = (select MAX(id_formulario) from formulario) and llave_formulario='FR-INSP-041.04';")
    for_emi = cursor.fetchall()
    cursor.execute(
        "select * from rep_foto_frpol where id_f = (select MAX(id) from frpol) ;")
    data = cursor.fetchall()
    cursor.execute(
        "select nom_inspe_formulario from formulario where id_formulario = (select MAX(b.id_formulario) from formulario a inner join frpol b on a.id_formulario = b.id_formulario);")
    nom_ins = cursor.fetchone()
    cursor.execute(
        "select * from equipos_ins where nombre_insp = %s and nombre in ('PIE DE REY','FLEXOMETRO','LUXOMETRO','TERMOMETRO INFRAROJO') or nombre = 'MEDIDOR DE SOLDADURA';" ,[nom_ins])
    data_ins = cursor.fetchall()
    print(nom_ins)
    return render_template('resumen_foto_pol.html', num_rep=num_rep,data=data, for_emi=for_emi,data_ins=data_ins)

@app.route('/cert_foto1', methods=['GET', 'POST'])
@login_required
def cert_foto1():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select * from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    for_emi = cursor.fetchall()
    cursor.execute(
        "select * from rep_foto_frpol where id_f = (select MAX(id) from frpol) ;")
    data = cursor.fetchall()

    return render_template('cert_foto1.html', data=data, for_emi=for_emi)

@app.route('/genera_pdffoto2')
@login_required
def genera_pdffoto2():
    options = {
        'dpi': '300',
        'page-size': 'A4',
        # 'orientation': 'Landscape',
        'margin-top': '0mm',
        'margin-right': '20mm',
        'margin-bottom': '20mm',
        'margin-left': '10mm',
        'encoding': "UTF-8",
        #'grayscale': None,
        'outline-depth':3,
        # 'footer-center':'[page]',
        'footer-line': None,
        "enable-local-file-access": None,
    }
    path = r'C:/Ricardo/paginas_web/u30/aplicacion/static/css/'
    css = [path + 'style.css']

    path_wkhtmltopdf = r'C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe'
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select * from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    for_emi = cursor.fetchall()
    cursor.execute(
        "select * from rep_foto_frpol where id_f = (select MAX(id) from frpol) ;")
    data = cursor.fetchall()
    html = render_template('resumen_foto_pol.html', data=data, for_emi=for_emi)
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    #pdfkit.from_file("aplicacion/templates/cert_for1.html", "index.pdf", options=options,configuration=config)
    pdfkit.from_string(html, "cert_foto1.pdf", options=options,configuration=config)
    #pdfkit.from_url("http://127.0.0.1:5000/cert_for1", "cert_for1.pdf",options=options,configuration=config)
    print("="*50)
    return redirect(url_for('cert_for1'))

@app.route('/genera_pdf1')
@login_required
def genera_pdf1():
    options = {
        'dpi': '300',
        'page-size': 'A4',
        # 'orientation': 'Landscape',
        'margin-top': '0mm',
        'margin-right': '20mm',
        'margin-bottom': '20mm',
        'margin-left': '10mm',
        'encoding': "UTF-8",
        #'grayscale': None,
        'outline-depth':3,
        # 'footer-center':'[page]',
        'footer-line': None,
        "enable-local-file-access": None,
    }
    path = r'C:/Ricardo/paginas_web/u30/aplicacion/static/css/'
    css = [path + 'style.css']

    path_wkhtmltopdf = r'C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe'
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select * from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    for_emi = cursor.fetchall()
    cursor.execute(
        "select fecha_expiracion_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_exp = cursor.fetchone()
    cursor.execute(
        "select llave_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    llave = cursor.fetchone()
    cursor.execute(
        "select lugar_ins_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    lug = cursor.fetchone()
    cursor.execute(
        "select nom_inspe_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    ins = cursor.fetchone()
    cursor.execute(
        "select * from frpol1 where id_f2 = (select MAX(id) from frpol) ;")
    data = cursor.fetchall()
    html = render_template('cert_for1.html', data=data, for_emi=for_emi, fec_exp=fec_exp, llave=llave, lug=lug, ins=ins)
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    #pdfkit.from_file("aplicacion/templates/cert_for1.html", "index.pdf", options=options,configuration=config)
    pdfkit.from_string(html, "cert_for1.pdf", options=options,configuration=config)
    #pdfkit.from_url("http://127.0.0.1:5000/cert_for1", "cert_for1.pdf",options=options,configuration=config)
    print("="*50)
    return redirect(url_for('inicio'))


@app.route('/genera_pdf2')
@login_required
def genera_pdf2():
    options = {
        'dpi': '300',
        'page-size': 'A4',
        # 'orientation': 'Landscape',
        'margin-top': '0mm',
        'margin-right': '20mm',
        'margin-bottom': '20mm',
        'margin-left': '10mm',
        'encoding': "UTF-8",
        #'grayscale': None,
        'outline-depth':3,
        # 'footer-center':'[page]',
        'footer-line': None,
        "enable-local-file-access": None,
    }
    path = r'C:/Ricardo/paginas_web/u30/aplicacion/static/css/'
    css = [path + 'style.css']

    path_wkhtmltopdf = r'C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe'
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select num_rep from formulario where id_formulario = (select MAX(b.id_formulario) from formulario a inner join frpol b on a.id_formulario = b.id_formulario);")
    num_rep = cursor.fetchone()
    cursor.execute(
        "select * from frpol where id_formulario = (select MAX(b.id_formulario) from formulario a inner join frpol b on a.id_formulario = b.id_formulario);")
    datos1 = cursor.fetchall()
    cursor.execute(
        "select MAX(id) from frpol ;")
    data1 = cursor.fetchone()
    cursor.execute(
        "select * from frpol1 where id_f2 = (select MAX(id) from frpol) ;")
    data = cursor.fetchall()
    cursor.execute(
        "select * from formulario where id_formulario = (select MAX(id_formulario) from formulario) and llave_formulario='FR-INSP-041.04';")
    for_emi = cursor.fetchall()
    cursor.execute(
        "select descr from cat_form where codigo = 'FR-INSP-043.03';")
    cata = cursor.fetchone()
    html = render_template('resum_frpol.html',num_rep=num_rep, datos1=datos1, contact=data1[0], data=data,for_emi=for_emi,cata=cata)
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    #pdfkit.from_file("aplicacion/templates/cert_for1.html", "index.pdf", options=options,configuration=config)
    pdfkit.from_string(html, "resum_frpol_1.pdf", options=options,configuration=config)
    #pdfkit.from_url("http://127.0.0.1:5000/cert_for1", "cert_for1.pdf",options=options,configuration=config)
    print("="*50)
    return redirect(url_for('reporte_fotopol'))





@app.route('/home_2', methods=['GET', 'POST'])
@login_required
def home_2():
    cursor = mysql.connection.cursor()
    cursor.execute("select nombre from articulos where id = 5;")
    nom_form = cursor.fetchone()
    cursor.execute("select descripcion from articulos where id = 5;")
    nom_form1 = cursor.fetchone()
    cur = mysql.connection.cursor()
    form = datos_reporte()
    if form.validate_on_submit():
        cur = mysql.connection.cursor()
        cur.execute("select (sec+1) from cod_rep where id = 14;")
        sec = cur.fetchone()
        print(sec)
        cur.execute("""
                    UPDATE cod_rep
                    SET sec = %s
                        WHERE id = 14
                """, sec)
        mysql.connection.commit()
        empre = request.form['empresa']
        cur.execute(
            "select CONCAT(prefijo,LPAD(sec, 5, '0')) from cod_rep where id_for = 3;")
        num_rep = cur.fetchone()
        fecha_insp = request.form['fec_inpec']
        fecha_emi = request.form['fec_emision']
        fecha_exp = request.form['fec_expiracion']
        lugar_ins = request.form['lugar_inpec']
        nombre_ins = request.form['nom_inspec']
        cursor = mysql.connection.cursor()
        cursor.execute('insert into formulario (llave_formulario,num_rep,desc_formulario,fecha_inspec_formulario,fecha_emision_formulario,fecha_expiracion_formulario,lugar_ins_formulario,nom_inspe_formulario,empresa,cod_form) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                       (nom_form,num_rep, nom_form1, fecha_insp, fecha_emi, fecha_exp, lugar_ins, nombre_ins, empre,'freca'))
        mysql.connection.commit()
        flash('Guardado Correctamente')
        datos = cursor.fetchone()
        # return 'OK'
        return redirect(url_for('freca'))
    return render_template('home_2.html', form=form, datos=nom_form, desc=nom_form1)


@app.route('/freca', methods=['GET', 'POST'])
@login_required
def freca():
    form = formu2()
    if form.validate_on_submit():
        revis = request.form['revis']
        nivel_il = request.form['nivel_il']
        con_sup = request.form['con_sup']
        met_insp = request.form['met_insp']
        tipo_il = request.form['tipo_il']
        check1 = request.form['check1']
        check2 = request.form['check2']
        check3 = request.form['check3']
        detalle = request.form['detalle']
        elem_ens = request.form['elem_ens']
        revis_p = request.form['revis_p']
        temp_ens = request.form['temp_ens']
        tipo_il_p = request.form['tipo_il_p']
        nivel_il_p = request.form['nivel_il_p']
        mater_base = request.form['mater_base']
        tipo_sec = request.form['tipo_sec']
        equipo = request.form['equipo']
        modelo = request.form['modelo']
        iden = request.form['iden']
        cur = mysql.connection.cursor()
        cur.execute(
            "select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
        llave_form = cur.fetchone()
        cur.execute(
            "select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
        fecha_form = cur.fetchone()
        cur.execute('insert into freca (id_formulario,fec_formulario,proc,revis,nivel_il,con_sup,met_insp,tipo_il,check1,check2,check3,detalle,elem_ens,proc_p,revis_p,temp_ens,tipo_il_p,nivel_il_p,mater_base,tipo_sec,tipo_pen,marca_kit,tiem_pen,met_rem,marca_kit1,tiem_sec,for_rev,marca_kit2,tiem_rev,equipo,modelo,iden) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                    (llave_form, fecha_form, 'PR-INSP-006', revis, nivel_il, con_sup, met_insp, tipo_il, check1, check2, check3, detalle,elem_ens, 'PR-INSP-007', revis_p, temp_ens, tipo_il_p, nivel_il_p, mater_base, tipo_sec, 'II VISIBLE', 'Met-L-Chek  VP-31A', '5 minutos', 'REMOVIBLE SOLVENTE', 'Met-L-Chek   E-59A', '10 minutos', 'SOLVENTE REMOVED', 'Met-L-Chek   D-70', '10 minutos', equipo, modelo, iden))
        mysql.connection.commit()
        return redirect(url_for('freca1'))
        # return render_template('formu_1_1.html', form=form)
    return render_template('freca.html', form=form)


@app.route('/add_freca1', methods=['POST'])
@login_required
def add_freca1():
    form = formu2_2()
    cur = mysql.connection.cursor()
    cur.execute("select (sec+1) from codigo where id_for = 3;")
    sec = cur.fetchone()
    cur.execute("""
            UPDATE codigo
            SET sec = %s
                WHERE id = 3
        """, sec)
    mysql.connection.commit()
    if form.validate_on_submit():
        ref = request.form['ref']
        cur.execute(
            "select CONCAT(preffijo,LPAD(sec, 4, '0')) from codigo where id_for = 3;")
        cod_enii = cur.fetchone()
        tipo_ter = request.form['tipo_ter']
        medidas = request.form['medidas']
        capac = request.form['capac']
        dia_elin = request.form['dia_elin']
        med_aces = request.form['med_aces']
        vt = request.form['vt']
        pt = request.form['pt']
        cur = mysql.connection.cursor()
        cur.execute(
            "select id from freca where id = (select MAX(id) from freca) ;")
        llave_form = cur.fetchone()
        print(llave_form)
        cur.execute('insert into freca1 (ref,cod_enii,tipo_ter,medidas,capac,dia_elin,med_aces,vt,pt,id_f3) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                    (ref, cod_enii, tipo_ter, medidas, capac, dia_elin, med_aces, vt, pt, llave_form))
        mysql.connection.commit()
        return redirect(url_for('freca1'))


@app.route('/freca1', methods=['GET', 'POST'])
@login_required
def freca1():
    form = formu2_2()
    cur = mysql.connection.cursor()
    cur.execute("select * from freca1 where id_f3=(select MAX(id) from freca) ;")
    data = cur.fetchall()
    return render_template('freca1.html', form=form, data=data)


@app.route('/edit_freca/<id>', methods=['POST', 'GET'])
@login_required
def get_contact1(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM freca WHERE id = %s', (id,))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-freca.html', contact=data[0])


@app.route('/update_freca/<id>', methods=['POST'])
@login_required
def update_freca(id):
    if request.method == 'POST':
        proc = request.form['proc']
        revis = request.form['revis']
        nivel_il = request.form['nivel_il']
        con_sup = request.form['con_sup']
        met_insp = request.form['met_insp']
        tipo_il = request.form['tipo_il']
        check1 = request.form['check1']
        check2 = request.form['check2']
        check3 = request.form['check3']
        detalle = request.form['detalle']
        elem_ens = request.form['elem_ens']
        proc_p = request.form['proc_p']
        revis_p = request.form['revis_p']
        temp_ens = request.form['temp_ens']
        tipo_il_p = request.form['tipo_il_p']
        nivel_il_p = request.form['nivel_il_p']
        mater_base = request.form['mater_base']
        tipo_sec = request.form['tipo_sec']
        tipo_pen = request.form['tipo_pen']
        marca_kit = request.form['marca_kit']
        tiem_pen = request.form['tiem_pen']
        met_rem = request.form['met_rem']
        marca_kit1 = request.form['marca_kit1']
        tiem_sec = request.form['tiem_sec']
        for_rev = request.form['for_rev']
        marca_kit2 = request.form['marca_kit2']
        tiem_rev = request.form['tiem_rev']
        equipo = request.form['equipo']
        modelo = request.form['modelo']
        iden = request.form['iden']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE freca
            SET proc = %s,
                revis = %s,
                nivel_il = %s,
				con_sup = %s,
                met_insp = %s,
				tipo_il = %s,
                check1 = %s,
				check2 = %s,
                check3 = %s,
				detalle = %s,
				elem_ens = %s,
                proc_p = %s,
				revis_p = %s,
                temp_ens = %s,
				tipo_il_p = %s,
                nivel_il_p = %s,
				mater_base = %s,
                tipo_sec = %s,
				tipo_pen = %s,
                marca_kit = %s,
				tiem_pen = %s,
                met_rem = %s,
				marca_kit1 = %s,
                tiem_sec = %s,
				for_rev = %s,
                marca_kit2 = %s,
				tiem_rev = %s,
                equipo = %s,
				modelo = %s,
                iden = %s
            WHERE id = %s
        """, (proc, revis, nivel_il, con_sup, met_insp, tipo_il, check1, check2, check3, detalle, elem_ens, proc_p, revis_p, temp_ens, tipo_il_p, nivel_il_p, mater_base, tipo_sec, tipo_pen, marca_kit, tiem_pen, met_rem, marca_kit1, tiem_sec, for_rev, marca_kit2, tiem_rev, equipo, modelo, iden, id))
        flash('Contact Updated Successfully')
        mysql.connection.commit()
        return redirect(url_for('resum_freca'))


@app.route('/edit_freca1/<id>', methods=['POST', 'GET'])
@login_required
def get_freca1(id):
    cur = mysql.connection.cursor()
    cur.execute(
        'SELECT * FROM freca1 WHERE num = %s and id_f3=(select MAX(id) from freca)',  [id])
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-freca1.html', contact=data[0])


@app.route('/update_freca1/<id>', methods=['POST'])
@login_required
def update_freca1(id):
    if request.method == 'POST':
        num = request.form['num']
        ref = request.form['ref']
        cod_enii = request.form['cod_enii']
        tipo_ter = request.form['tipo_ter']
        medidas = request.form['medidas']
        capac = request.form['capac']
        dia_elin = request.form['dia_elin']
        med_aces = request.form['med_aces']
        vt = request.form['vt']
        pt = request.form['pt']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE freca1
            SET num = %s,
                ref = %s,
                cod_enii = %s,
                tipo_ter = %s,
				medidas = %s,
                capac = %s,
				dia_elin = %s,
				med_aces = %s,
                vt = %s,
				pt = %s
            WHERE num = %s
        """, (num, ref, cod_enii, tipo_ter, medidas, capac, dia_elin, med_aces, vt, pt, num))
        flash('Contact Updated Successfully')
        mysql.connection.commit()
        return redirect(url_for('freca1'))


@app.route('/resum_freca')
@login_required
def resum_freca():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select num_rep from formulario where id_formulario = (select MAX(b.id_formulario) from formulario a inner join freca b on a.id_formulario = b.id_formulario);")
    num_rep = cursor.fetchone()
    cursor.execute(
        "select * from formulario where id_formulario = (select MAX(id_formulario) from formulario) and llave_formulario='FR-INSP-042.00';")
    for_emi = cursor.fetchone()
    cursor.execute(
        "select * from freca where id_formulario = (select MAX(b.id_formulario) from formulario a inner join freca b on a.id_formulario = b.id_formulario);")
    datos1 = cursor.fetchall()
    cursor.execute(
        "select MAX(id) from freca ;")
    data1 = cursor.fetchone()
    cursor.execute(
        "select * from freca1 where id_f3 = (select MAX(id) from freca) ;")
    data = cursor.fetchall()
    cursor.execute(
        "select descr from cat_form where codigo = 'FR-INSP-043.03';")
    cata = cursor.fetchone()
    print(cata)
    return render_template('resum_freca.html', num_rep=num_rep,for_emi=for_emi, datos1=datos1, contact=data1[0], data=data,cata=cata)



@app.route('/reporte_fotofreca')
@login_required
def reporte_fotofreca():
    lista = []
    for file in listdir(app.root_path+"/static/img/subidas/freca/"):
        lista.append(file)
    return render_template("reporte_fotofreca.html", lista=lista)


@app.route('/upload_freca', methods=['get', 'post'])
def upload_freca():
    form = UploadForm()  # carga request.from y request.file
    if form.validate_on_submit():
        f = form.photo.data
        filename = secure_filename(f.filename)
        f.save(app.root_path+"/static/img/subidas/freca/"+filename)
        foto = app.root_path+"/static/img/subidas/freca/"+filename
        cursor = mysql.connection.cursor()
        cursor.execute(
            "select id from freca where id = (select MAX(id) from freca) ;")
        llave_form = cursor.fetchone()
        cursor.execute('insert into rep_foto_freca (foto,id_f) VALUES (%s,%s)',
                    ( foto,llave_form))
        mysql.connection.commit()
        return redirect(url_for('inicio_fotofreca'))
    return render_template('upload_freca.html', form=form)

@app.route('/inicio_fotofreca')
@login_required
def inicio_fotofreca():
    lista = []
    for file in listdir(app.root_path+"/static/img/subidas/freca/"):
        lista.append(file)
    return render_template("inicio_fotofreca.html", lista=lista)



@app.route('/cert_for2', methods=['GET', 'POST'])
@login_required
def cert_for2():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select fecha_emision_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_emi = cursor.fetchone()
    cursor.execute(
        "select fecha_expiracion_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_exp = cursor.fetchone()
    cursor.execute(
        "select llave_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    llave = cursor.fetchone()
    cursor.execute(
        "select lugar_ins_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    lug = cursor.fetchone()
    cursor.execute(
        "select nom_inspe_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    ins = cursor.fetchone()
    cursor.execute(
        "select * from freca1 where id_f3 = (select MAX(id) from freca) ;")
    data = cursor.fetchall()

    return render_template('cert_for2.html', data=data, fec_emi=fec_emi, fec_exp=fec_exp, llave=llave, lug=lug, ins=ins)


@app.route('/genera_pdffreca')
@login_required
def genera_pdffreca():
    options = {
        'dpi': '300',
        'page-size': 'A4',
        # 'orientation': 'Landscape',
        'margin-top': '0mm',
        'margin-right': '20mm',
        'margin-bottom': '20mm',
        'margin-left': '10mm',
        'encoding': "UTF-8",
        'outline-depth':3,
        # 'footer-center':'[page]',
        'footer-line': None,
        "enable-local-file-access": None,
    }
    path_wkhtmltopdf = r'C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe'
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select fecha_emision_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_emi = cursor.fetchone()
    cursor.execute(
        "select fecha_expiracion_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_exp = cursor.fetchone()
    cursor.execute(
        "select llave_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    llave = cursor.fetchone()
    cursor.execute(
        "select lugar_ins_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    lug = cursor.fetchone()
    cursor.execute(
        "select nom_inspe_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    ins = cursor.fetchone()
    cursor.execute(
        "select * from freca1 where id_f3 = (select MAX(id) from freca) ;")
    data = cursor.fetchall()
    html = render_template('cert_for2.html', data=data, fec_emi=fec_emi, fec_exp=fec_exp, llave=llave, lug=lug, ins=ins)
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    #pdfkit.from_file("aplicacion/templates/cert_for1.html", "index.pdf", options=options,configuration=config)
    pdfkit.from_string(html, "cert_for2.pdf", options=options,configuration=config)
    print("="*50)
    return redirect(url_for('inicio'))


@app.route('/genera_pdffreca2')
@login_required
def genera_pdffreca2():
    options = {
        'dpi': '300',
        'page-size': 'A4',
        # 'orientation': 'Landscape',
        'margin-top': '0mm',
        'margin-right': '20mm',
        'margin-bottom': '20mm',
        'margin-left': '10mm',
        'encoding': "UTF-8",
        #'grayscale': None,
        'outline-depth':3,
        # 'footer-center':'[page]',
        'footer-line': None,
        "enable-local-file-access": None,
    }
    path = r'C:/Ricardo/paginas_web/u30/aplicacion/static/css/'
    css = [path + 'style.css']

    path_wkhtmltopdf = r'C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe'
    cursor = mysql.connection.cursor()
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select llave_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    nom_form = cursor.fetchone()
    cursor.execute(
        "select num_rep from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    num_rep = cursor.fetchone()
    cursor.execute(
        "select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_insp = cursor.fetchone()
    cursor.execute(
        "select fecha_emision_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_emi = cursor.fetchone()
    cursor.execute(
        "select fecha_expiracion_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_exp = cursor.fetchone()
    cursor.execute(
        "select lugar_ins_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    lugar = cursor.fetchone()
    cursor.execute(
        "select nom_inspe_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    inpe = cursor.fetchone()
    cursor.execute(
        "select * from freca where id_formulario = (select MAX(id_formulario) from formulario);")
    datos1 = cursor.fetchall()
    cursor.execute(
        "select MAX(id) from freca ;")
    data1 = cursor.fetchone()
    cursor.execute(
        "select * from freca1 where id_f3 = (select MAX(id) from freca) ;")
    data = cursor.fetchall()
    html = render_template('resum_freca_1.html', datos=nom_form,num_rep=num_rep, fec1=fec_insp, fec2=fec_emi, fec3=fec_exp, lugar=lugar, inspector=inpe, datos1=datos1, contact=data1[0], data=data)
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    #pdfkit.from_file("aplicacion/templates/cert_for1.html", "index.pdf", options=options,configuration=config)
    pdfkit.from_string(html, "resum_freca_1.pdf", options=options,configuration=config)
    #pdfkit.from_url("http://127.0.0.1:5000/cert_for1", "cert_for1.pdf",options=options,configuration=config)
    print("="*50)
    return redirect(url_for('cert_for2'))


@app.route('/home_3', methods=['GET', 'POST'])
@login_required
def home_3():
    cursor = mysql.connection.cursor()
    cursor.execute("select nombre from articulos where id = 10;")
    nom_form = cursor.fetchone()
    cursor.execute("select descripcion from articulos where id = 10;")
    nom_form1 = cursor.fetchone()
    form = datos_reporte()
    if form.validate_on_submit():
        cur = mysql.connection.cursor()
        cur.execute("select (sec+1) from cod_rep where id = 15;")
        sec = cur.fetchone()
        print(sec)
        cur.execute("""
                    UPDATE cod_rep
                    SET sec = %s
                        WHERE id = 15
                """, sec)
        mysql.connection.commit()
        empre = request.form['empresa']
        cur.execute(
            "select CONCAT(prefijo,LPAD(sec, 5, '0')) from cod_rep where id_for = 4;")
        num_rep = cur.fetchone()
        empre = request.form['empresa']
        fecha_insp = request.form['fec_inpec']
        fecha_emi = request.form['fec_emision']
        fecha_exp = request.form['fec_expiracion']
        lugar_ins = request.form['lugar_inpec']
        nombre_ins = request.form['nom_inspec']
        cursor = mysql.connection.cursor()
        cursor.execute('insert into formulario (llave_formulario,num_rep,desc_formulario,fecha_inspec_formulario,fecha_emision_formulario,fecha_expiracion_formulario,lugar_ins_formulario,nom_inspe_formulario,empresa,cod_form) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                       (nom_form,num_rep, nom_form1, fecha_insp, fecha_emi, fecha_exp, lugar_ins, nombre_ins, empre,'frcad'))
        mysql.connection.commit()
        flash('Guardado Correctamente')
        datos = cursor.fetchone()
        print(datos)
        # return 'OK'
        return redirect(url_for('frcad'))
    return render_template('home_3.html', form=form, datos=nom_form, desc=nom_form1)


@app.route('/frcad', methods=['GET', 'POST'])
@login_required
def frcad():
    form = formu3()
    if form.validate_on_submit():
        revis = request.form['revis']
        nivel_il = request.form['nivel_il']
        con_sup = request.form['con_sup']
        met_insp = request.form['met_insp']
        tipo_il = request.form['tipo_il']
        check1 = request.form['check1']
        check2 = request.form['check2']
        check3 = request.form['check3']
        detalle = request.form['detalle']
        revis_p = request.form['revis_p']
        temp_ens = request.form['temp_ens']
        tipo_il_p = request.form['tipo_il_p']
        nivel_il_p = request.form['nivel_il_p']
        mater_base = request.form['mater_base']
        tipo_sec = request.form['tipo_sec']
        equipo = request.form['equipo']
        modelo = request.form['modelo']
        iden = request.form['iden']
        cur = mysql.connection.cursor()
        cur.execute(
            "select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
        llave_form = cur.fetchone()
        cur.execute(
            "select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
        fecha_form = cur.fetchone()
        cur.execute('insert into frcad (id_formulario,fec_formulario,proc,revis,nivel_il,con_sup,met_insp,tipo_il,check1,check2,check3,detalle,proc_p,revis_p,temp_ens,tipo_il_p,nivel_il_p,mater_base,tipo_sec,tipo_pen,marca_kit,tiem_pen,met_rem,marca_kit1,tiem_sec,for_rev,marca_kit2,tiem_rev,equipo,modelo,iden) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                    (llave_form, fecha_form, 'PR-INSP-006', revis, nivel_il, con_sup, met_insp, tipo_il, check1, check2, check3, detalle, 'PR-INSP-007', revis_p, temp_ens, tipo_il_p, nivel_il_p, mater_base, tipo_sec,'II VISIBLE', 'Met-L-Chek  VP-31A', '5 minutos', 'REMOVIBLE SOLVENTE', 'Met-L-Chek   E-59A', '10 minutos', 'SOLVENTE REMOVED', 'Met-L-Chek   D-70', '10 minutos', equipo, modelo, iden,))
        mysql.connection.commit()
        return redirect(url_for('frcad1'))
    return render_template('frcad.html', form=form)


@app.route('/add_frcad1', methods=['POST'])
@login_required
def add_frcad1():
    form = formu3_3()
    cur = mysql.connection.cursor()
    cur.execute("select (sec+1) from codigo where id_for = 4;")
    sec = cur.fetchone()
    cur.execute("""
            UPDATE codigo
            SET sec = %s
                WHERE id = 4
        """, sec)
    mysql.connection.commit()
    if form.validate_on_submit():
        tipo_ace = request.form['tipo_ace']
        ref = request.form['ref']
        cur.execute(
            "select CONCAT(preffijo,LPAD(sec, 5, '0')) from codigo where id_for = 4;")
        cod_enii = cur.fetchone()
        eslabon = request.form['eslabon']
        medidas = request.form['medidas']
        capac = request.form['capac']
        gancho1 = request.form['gancho1']
        gancho2 = request.form['gancho2']
        vt = request.form['vt']
        pt = request.form['pt']
        cur = mysql.connection.cursor()
        cur.execute(
            "select id from frcad where id = (select MAX(id) from frcad) ;")
        llave_form = cur.fetchone()
        print(llave_form)
        cur.execute('insert into frcad1 (tipo_ace,ref,cod_enii,eslabon,medidas,capac,gancho1,gancho2,vt,pt,id_f4) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                    (tipo_ace, ref, cod_enii, eslabon, medidas, capac, gancho1, gancho2, vt, pt, llave_form))
        mysql.connection.commit()
        return redirect(url_for('frcad1'))


@app.route('/frcad1', methods=['GET', 'POST'])
@login_required
def frcad1():
    form = formu3_3()
    cur = mysql.connection.cursor()
    cur.execute("select * from frcad1 where id_f4=(select MAX(id) from frcad) ;")
    data = cur.fetchall()
    return render_template('frcad1.html', form=form, data=data)


@app.route('/edit_frcad/<id>', methods=['POST', 'GET'])
@login_required
def get_contact2(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM frcad WHERE id = %s', (id,))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-frcad.html', contact=data[0])


@app.route('/update_frcad/<id>', methods=['POST'])
@login_required
def update_frcad(id):
    if request.method == 'POST':
        proc = request.form['proc']
        revis = request.form['revis']
        nivel_il = request.form['nivel_il']
        con_sup = request.form['con_sup']
        met_insp = request.form['met_insp']
        tipo_il = request.form['tipo_il']
        check1 = request.form['check1']
        check2 = request.form['check2']
        check3 = request.form['check3']
        detalle = request.form['detalle']
        elem_ens = request.form['elem_ens']
        proc_p = request.form['proc_p']
        revis_p = request.form['revis_p']
        temp_ens = request.form['temp_ens']
        tipo_il_p = request.form['tipo_il_p']
        nivel_il_p = request.form['nivel_il_p']
        mater_base = request.form['mater_base']
        tipo_sec = request.form['tipo_sec']
        tipo_pen = request.form['tipo_pen']
        marca_kit = request.form['marca_kit']
        tiem_pen = request.form['tiem_pen']
        met_rem = request.form['met_rem']
        marca_kit1 = request.form['marca_kit1']
        tiem_sec = request.form['tiem_sec']
        for_rev = request.form['for_rev']
        marca_kit2 = request.form['marca_kit2']
        tiem_rev = request.form['tiem_rev']
        equipo = request.form['equipo']
        modelo = request.form['modelo']
        iden = request.form['iden']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE freca
            SET proc = %s,
                revis = %s,
                nivel_il = %s,
				con_sup = %s,
                met_insp = %s,
				tipo_il = %s,
                check1 = %s,
				check2 = %s,
                check3 = %s,
				detalle = %s,
				elem_ens = %s,
                proc_p = %s,
				revis_p = %s,
                temp_ens = %s,
				tipo_il_p = %s,
                nivel_il_p = %s,
				mater_base = %s,
                tipo_sec = %s,
				tipo_pen = %s,
                marca_kit = %s,
				tiem_pen = %s,
                met_rem = %s,
				marca_kit1 = %s,
                tiem_sec = %s,
				for_rev = %s,
                marca_kit2 = %s,
				tiem_rev = %s,
                equipo = %s,
				modelo = %s,
                iden = %s
            WHERE id = %s
        """, (proc, revis, nivel_il, con_sup, met_insp, tipo_il, check1, check2, check3, detalle, elem_ens, proc_p, revis_p, temp_ens, tipo_il_p, nivel_il_p, mater_base, tipo_sec, tipo_pen, marca_kit, tiem_pen, met_rem, marca_kit1, tiem_sec, for_rev, marca_kit2, tiem_rev, equipo, modelo, iden, id))
        flash('Contact Updated Successfully')
        mysql.connection.commit()
        return redirect(url_for('resum_frcad'))


@app.route('/edit_frcad1/<id>', methods=['POST', 'GET'])
@login_required
def get_f33(id):
    cur = mysql.connection.cursor()
    cur.execute(
        'SELECT * FROM frcad1 WHERE num = %s and id_f4=(select MAX(id) from frcad)', [id])
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-frcad1.html', contact=data[0])


@app.route('/update_frcad1/<id>', methods=['POST'])
@login_required
def update_frcad1(id):
    if request.method == 'POST':
        num = request.form['num']
        ref = request.form['ref']
        cod_enii = request.form['cod_enii']
        tipo_ace = request.form['tipo_ace']
        medidas = request.form['medidas']
        capac = request.form['capac']
        eslabon = request.form['eslabon']
        gancho1 = request.form['gancho1']
        gancho2 = request.form['gancho2']
        vt = request.form['vt']
        pt = request.form['pt']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE frcad1
            SET tipo_ace = %s,
                num = %s,
                cod_enii = %s,
                ref = %s,				
				medidas = %s,
                capac = %s,
				eslabon = %s,
				gancho1 = %s,
                gancho2 = %s,
                vt = %s,
				pt = %s
            WHERE num = %s
        """, (tipo_ace, num, cod_enii, ref, medidas, capac, eslabon, gancho1, gancho2, vt, pt, num))
        flash('Contact Updated Successfully')
        mysql.connection.commit()
        return redirect(url_for('frcad1'))


@app.route('/resum_frcad')
@login_required
def resum_frcad():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select * from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    datos = cursor.fetchall()
    cursor.execute(
        "select num_rep from formulario where id_formulario = (select MAX(b.id_formulario) from formulario a inner join frcad b on a.id_formulario = b.id_formulario);")
    num_rep = cursor.fetchone()
    cursor.execute(
        "select * from frcad where id_formulario = (select MAX(b.id_formulario) from formulario a inner join frcad b on a.id_formulario = b.id_formulario);")
    datos1 = cursor.fetchall()
    cursor.execute(
        "select MAX(id) from frcad ;")
    data1 = cursor.fetchone()
    cursor.execute(
        "select * from frcad1 where id_f4 = (select MAX(id) from frcad) ;")
    data = cursor.fetchall()
    cursor.execute(
        "select descr from cat_form where codigo = 'FR-INSP-045.04';")
    cata = cursor.fetchone()
    print(data)
    return render_template('resum_frcad.html', datos=datos, num_rep=num_rep, datos1=datos1, contact=data1[0], data=data,cata=cata)


@app.route('/genera_pdffrcad2')
@login_required
def genera_pdffrcad2():
    options = {
        'dpi': '300',
        'page-size': 'A4',
        # 'orientation': 'Landscape',
        'margin-top': '0mm',
        'margin-right': '20mm',
        'margin-bottom': '20mm',
        'margin-left': '10mm',
        'encoding': "UTF-8",
        #'grayscale': None,
        'outline-depth':3,
        # 'footer-center':'[page]',
        'footer-line': None,
        "enable-local-file-access": None,
    }
    path = r'C:/Ricardo/paginas_web/u30/aplicacion/static/css/'
    css = [path + 'style.css']

    path_wkhtmltopdf = r'C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe'
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select llave_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    nom_form = cursor.fetchone()
    cursor.execute(
        "select num_rep from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    num_rep = cursor.fetchone()
    cursor.execute(
        "select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_insp = cursor.fetchone()
    cursor.execute(
        "select fecha_emision_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_emi = cursor.fetchone()
    cursor.execute(
        "select fecha_expiracion_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_exp = cursor.fetchone()
    cursor.execute(
        "select lugar_ins_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    lugar = cursor.fetchone()
    cursor.execute(
        "select nom_inspe_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    inpe = cursor.fetchone()
    cursor.execute(
        "select * from frcad where id_formulario = (select MAX(id_formulario) from formulario);")
    datos1 = cursor.fetchall()
    cursor.execute(
        "select MAX(id) from frcad ;")
    data1 = cursor.fetchone()
    cursor.execute(
        "select * from frcad1 where id_f4 = (select MAX(id) from frcad) ;")
    data = cursor.fetchall()
    html = render_template('resum_frcad_1.html', datos=nom_form, num_rep=num_rep,fec1=fec_insp, fec2=fec_emi, fec3=fec_exp, lugar=lugar, inspector=inpe, datos1=datos1, contact=data1[0], data=data)
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    #pdfkit.from_file("aplicacion/templates/cert_for1.html", "index.pdf", options=options,configuration=config)
    pdfkit.from_string(html, "resum_frcad_1.pdf", options=options,configuration=config)
    #pdfkit.from_url("http://127.0.0.1:5000/cert_for1", "cert_for1.pdf",options=options,configuration=config)
    print("="*50)
    return redirect(url_for('cert_for3'))

@app.route('/reporte_fotofrcad')
@login_required
def reporte_fotofrcad():
    lista = []
    for file in listdir(app.root_path+"/static/img/subidas/pol/"):
        lista.append(file)
    return render_template("reporte_fotofrcad.html", lista=lista)


@app.route('/upload_frcad', methods=['get', 'post'])
def upload_frcad():
    form = UploadForm()  # carga request.from y request.file
    if form.validate_on_submit():
        f = form.photo.data
        filename = secure_filename(f.filename)
        f.save(app.root_path+"/static/img/subidas/frcad/"+filename)
        foto = app.root_path+"/static/img/subidas/frcad/"+filename
        cursor = mysql.connection.cursor()
        cursor.execute(
            "select id from frcad where id = (select MAX(id) from frcad) ;")
        llave_form = cursor.fetchone()
        cursor.execute('insert into rep_foto_frcad (foto,id_f) VALUES (%s,%s)',
                    ( foto,llave_form))
        mysql.connection.commit()
        return redirect(url_for('inicio_fotofrcad'))
    return render_template('upload_frcad.html', form=form)

@app.route('/inicio_fotofrcad')
@login_required
def inicio_fotofrcad():
    lista = []
    for file in listdir(app.root_path+"/static/img/subidas/freca/"):
        lista.append(file)
    return render_template("inicio_fotofrcad.html", lista=lista)



@app.route('/cert_for3', methods=['GET', 'POST'])
@login_required
def cert_for3():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select fecha_emision_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_emi = cursor.fetchone()
    cursor.execute(
        "select fecha_expiracion_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_exp = cursor.fetchone()
  
    cursor.execute(
        "select llave_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    llave = cursor.fetchone()
    cursor.execute(
        "select lugar_ins_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    lug = cursor.fetchone()
    cursor.execute(
        "select nom_inspe_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    ins = cursor.fetchone()
    cursor.execute(
        "select * from frcad1 where id_f4 = (select MAX(id) from frcad) ;")
    data = cursor.fetchall()

    return render_template('cert_for3.html', data=data, fec_emi=fec_emi, fec_exp=fec_exp, llave=llave, lug=lug, ins=ins)



@app.route('/genera_pdffrcad')
@login_required
def genera_pdffrcad():
    options = {
        'page-size': 'A4',
        # 'orientation': 'Landscape',
        'margin-top': '20mm',
        'margin-right': '20mm',
        'margin-bottom': '20mm',
        'margin-left': '20mm',
        'encoding': "UTF-8",
        'outline-depth':3,
        # 'footer-center':'[page]',
        'footer-line': None,
        "enable-local-file-access": None,
    }
    path_wkhtmltopdf = r'C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe'
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select fecha_emision_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_emi = cursor.fetchone()
    cursor.execute(
        "select fecha_expiracion_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_exp = cursor.fetchone()
    cursor.execute(
        "select llave_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    llave = cursor.fetchone()
    cursor.execute(
        "select lugar_ins_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    lug = cursor.fetchone()
    cursor.execute(
        "select nom_inspe_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    ins = cursor.fetchone()
    cursor.execute(
        "select * from frcad1 where id_f4 = (select MAX(id) from frcad) ;")
    data = cursor.fetchall()
    html = render_template('cert_for3.html', data=data, fec_emi=fec_emi, fec_exp=fec_exp, llave=llave, lug=lug, ins=ins)
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    #pdfkit.from_file("aplicacion/templates/cert_for1.html", "index.pdf", options=options,configuration=config)
    pdfkit.from_string(html, "cert_for3.pdf", options=options,configuration=config)
    print("="*50)
    return redirect(url_for('inicio'))



@app.route('/home_4', methods=['GET', 'POST'])
@login_required
def home_4():
    cursor = mysql.connection.cursor()
    cursor.execute("select nombre from articulos where id = 7;")
    nom_form = cursor.fetchone()
    cursor.execute("select descripcion from articulos where id = 7;")
    nom_form1 = cursor.fetchone()
    form = datos_reporte()
    if form.validate_on_submit():
        cur = mysql.connection.cursor()
        cur.execute("select (sec+1) from cod_rep where id = 16;")
        sec = cur.fetchone()
        print(sec)
        cur.execute("""
                    UPDATE cod_rep
                    SET sec = %s
                        WHERE id = 16
                """, sec)
        mysql.connection.commit()
        empre = request.form['empresa']
        cur.execute(
            "select CONCAT(prefijo,LPAD(sec, 5, '0')) from cod_rep where id_for = 5;")
        num_rep = cur.fetchone()
        empre = request.form['empresa']
        fecha_insp = request.form['fec_inpec']
        fecha_emi = request.form['fec_emision']
        fecha_exp = request.form['fec_expiracion']
        lugar_ins = request.form['lugar_inpec']
        nombre_ins = request.form['nom_inspec']
        cursor = mysql.connection.cursor()
        cursor.execute('insert into formulario (llave_formulario,num_rep,desc_formulario,fecha_inspec_formulario,fecha_emision_formulario,fecha_expiracion_formulario,lugar_ins_formulario,nom_inspe_formulario,empresa,cod_form) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                       (nom_form,num_rep, nom_form1, fecha_insp, fecha_emi, fecha_exp, lugar_ins, nombre_ins, empre,'frefs'))
        mysql.connection.commit()
        flash('Guardado Correctamente')
        datos = cursor.fetchone()
        print(datos)
        # return 'OK'
        return redirect(url_for('frefs'))
    return render_template('home_4.html', form=form, datos=nom_form, desc=nom_form1)


@app.route('/frefs', methods=['GET', 'POST'])
@login_required
def frefs():
    form = formu4()
    if form.validate_on_submit():
        revis = request.form['revis']
        nivel_il = request.form['nivel_il']
        con_sup = request.form['con_sup']
        met_insp = request.form['met_insp']
        tipo_il = request.form['tipo_il']
        check1 = request.form['check1']
        check2 = request.form['check2']
        check3 = request.form['check3']
        detalle = request.form['detalle']
        equipo = request.form['equipo']
        modelo = request.form['modelo']
        iden = request.form['iden']
        cur = mysql.connection.cursor()
        cur.execute(
            "select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
        llave_form = cur.fetchone()
        cur.execute(
            "select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
        fecha_form = cur.fetchone()
        cur.execute('insert into frefs (id_formulario,fec_formulario,proc,revis,nivel_il,con_sup,met_insp,tipo_il,check1,check2,check3,detalle,equipo,modelo,iden) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                    (llave_form, fecha_form, 'PR-INSP-006', revis, nivel_il, con_sup, met_insp, tipo_il, check1, check2, check3, detalle, equipo, modelo, iden))
        mysql.connection.commit()
        return redirect(url_for('frefs1'))
    return render_template('frefs.html', form=form)


@app.route('/edit_frefs/<id>', methods=['POST', 'GET'])
@login_required
def get_frefs(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM frefs WHERE id = %s', (id,))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-frefs.html', contact=data[0])

@app.route('/add_frefs1', methods=['POST'])
@login_required
def add_frefs1():
    form = formu4_4()
    cur = mysql.connection.cursor()
    cur.execute("select (sec+1) from codigo where id_for = 5;")
    sec = cur.fetchone()
    cur.execute("""
            UPDATE codigo
            SET sec = %s
                WHERE id = 5
        """, sec)
    mysql.connection.commit()
    if form.validate_on_submit():
        cur = mysql.connection.cursor()
        ref = request.form['ref']
        tipo = request.form['tipo']
        medidas = request.form['medidas']
        capac = request.form['capac']
        vt = request.form['vt']
        cur.execute(
            "select CONCAT(preffijo,LPAD(sec, 4, '0')) from codigo where id_for = 5;")
        cod_enii = cur.fetchone()
        cur.execute(
            "select id from frefs where id = (select MAX(id) from frefs) ;")
        llave_form = cur.fetchone()
        print(cod_enii)
        cur.execute('insert into frefs1 (ref,cod_enii,tipo,medidas,capac,vt,id_f5) VALUES (%s,%s,%s,%s,%s,%s,%s)',
                    ( ref, cod_enii, tipo, medidas, capac, vt, llave_form))
        mysql.connection.commit()
        return redirect(url_for('frefs1'))


@app.route('/frefs1', methods=['GET', 'POST'])
@login_required
def frefs1():
    form = formu4_4()
    cur = mysql.connection.cursor()
    cur.execute("select * from frefs1 where id_f5=(select MAX(id) from frefs) ;")
    data = cur.fetchall()
    return render_template('frefs1.html', form=form, data=data)


@app.route('/edit-frefs1/<id>', methods=['POST', 'GET'])
@login_required
def get_f44(id):
    cur = mysql.connection.cursor()
    cur.execute(
        'SELECT * FROM frefs1 WHERE num = %s and id_f5 = (select MAX(id) from frefs)', (id,))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-frefs1.html', contact=data[0])


@app.route('/update_frefs/<id>', methods=['POST'])
@login_required
def update_frefs(id):
    if request.method == 'POST':
        proc = request.form['proc']
        revis = request.form['revis']
        nivel_il = request.form['nivel_il']
        con_sup = request.form['con_sup']
        met_insp = request.form['met_insp']
        tipo_il = request.form['tipo_il']
        check1 = request.form['check1']
        check2 = request.form['check2']
        check3 = request.form['check3']
        detalle = request.form['detalle']
        equipo = request.form['equipo']
        modelo = request.form['modelo']
        iden = request.form['iden']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE frpol
            SET proc = %s,
                revis = %s,
                nivel_il = %s,
				con_sup = %s,
                met_insp = %s,
				tipo_il = %s,
                check1 = %s,
				check2 = %s,
                check3 = %s,
				detalle = %s,
                equipo = %s,
				modelo = %s,
                iden = %s
            WHERE id = %s
        """, (proc, revis, nivel_il, con_sup, met_insp, tipo_il, check1, check2, check3, detalle, equipo, modelo, iden, id))
        flash('Contact Updated Successfully')
        mysql.connection.commit()
        return redirect(url_for('resumen4'))


@app.route('/update_frefs1/<id>', methods=['POST'])
@login_required
def update_frefs1(id):
    if request.method == 'POST':
        num = request.form['num']
        ref = request.form['ref']
        cod_enii = request.form['cod_enii']
        tipo = request.form['tipo']
        medidas = request.form['medidas']
        capac = request.form['capac']
        vt = request.form['vt']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE frefs1
            SET num = %s,
                ref = %s,
                cod_enii = %s,
				tipo = %s,
                medidas = %s,
                capac = %s,
				vt = %s
            WHERE num = %s
        """, (num, ref, cod_enii, tipo, medidas, capac, vt, num))
        flash('Contact Updated Successfully')
        mysql.connection.commit()
        return redirect(url_for('frefs1'))


@app.route('/resum_frefs')
@login_required
def resum_frefs():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select * from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    datos = cursor.fetchone()
    cursor.execute(
        "select num_rep from formulario where id_formulario = (select MAX(b.id_formulario) from formulario a inner join frefs b on a.id_formulario = b.id_formulario);")
    num_rep = cursor.fetchone()
    cursor.execute(
        "select * from frefs where id_formulario = (select MAX(b.id_formulario) from formulario a inner join frefs b on a.id_formulario = b.id_formulario);")
    datos1 = cursor.fetchall()
    cursor.execute(
        "select MAX(id) from frefs ;")
    data1 = cursor.fetchone()
    cursor.execute(
        "select * from frefs1 where id_f5 = (select MAX(id) from frefs) ;")
    data = cursor.fetchall()
    cursor.execute(
        "select descr from cat_form where codigo = 'FR-INSP-047.03';")
    cata = cursor.fetchone()
    print(data)
    return render_template('resum_frefs.html', datos=datos,num_rep=num_rep,datos1=datos1, contact=data1[0], data=data,cata=cata)


@app.route('/genera_pdffrefs2')
@login_required
def genera_pdffrefs2():
    options = {
        'dpi': '300',
        'page-size': 'A4',
        # 'orientation': 'Landscape',
        'margin-top': '0mm',
        'margin-right': '20mm',
        'margin-bottom': '20mm',
        'margin-left': '10mm',
        'encoding': "UTF-8",
        #'grayscale': None,
        'outline-depth':3,
        # 'footer-center':'[page]',
        'footer-line': None,
        "enable-local-file-access": None,
    }
    path = r'C:/Ricardo/paginas_web/u30/aplicacion/static/css/'
    css = [path + 'style.css']

    path_wkhtmltopdf = r'C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe'
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select llave_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    nom_form = cursor.fetchone()
    cursor.execute(
        "select num_rep from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    num_rep = cursor.fetchone()
    cursor.execute(
        "select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_insp = cursor.fetchone()
    cursor.execute(
        "select fecha_emision_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_emi = cursor.fetchone()
    cursor.execute(
        "select fecha_expiracion_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_exp = cursor.fetchone()
    cursor.execute(
        "select lugar_ins_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    lugar = cursor.fetchone()
    cursor.execute(
        "select nom_inspe_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    inpe = cursor.fetchone()
    cursor.execute(
        "select * from frefs where id_formulario = (select MAX(id_formulario) from formulario);")
    datos1 = cursor.fetchall()
    cursor.execute(
        "select MAX(id) from frefs ;")
    data1 = cursor.fetchone()
    cursor.execute(
        "select * from frefs1 where id_f5 = (select MAX(id) from frefs) ;")
    data = cursor.fetchall()
    html = render_template('resum_frefs_1.html', datos=nom_form,num_rep=num_rep, fec1=fec_insp, fec2=fec_emi, fec3=fec_exp, lugar=lugar, inspector=inpe, datos1=datos1, contact=data1[0], data=data)
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    #pdfkit.from_file("aplicacion/templates/cert_for1.html", "index.pdf", options=options,configuration=config)
    pdfkit.from_string(html, "resum_frefs_1.pdf", options=options,configuration=config)
    #pdfkit.from_url("http://127.0.0.1:5000/cert_for1", "cert_for1.pdf",options=options,configuration=config)
    print("="*50)
    return redirect(url_for('cert_for4'))

@app.route('/reporte_fotofrefs')
@login_required
def reporte_fotofrefs():
    lista = []
    for file in listdir(app.root_path+"/static/img/subidas/frefs/"):
        lista.append(file)
    return render_template("reporte_fotofrefs.html", lista=lista)


@app.route('/upload_frefs', methods=['get', 'post'])
def upload_frefs():
    form = UploadForm()  # carga request.from y request.file
    if form.validate_on_submit():
        f = form.photo.data
        filename = secure_filename(f.filename)
        f.save(app.root_path+"/static/img/subidas/frefs/"+filename)
        foto = app.root_path+"/static/img/subidas/frefs/"+filename
        cursor = mysql.connection.cursor()
        cursor.execute(
            "select id from frefs where id = (select MAX(id) from frefs) ;")
        llave_form = cursor.fetchone()
        cursor.execute('insert into rep_foto_frefs (foto,id_f) VALUES (%s,%s)',
                    ( foto,llave_form))
        mysql.connection.commit()
        return redirect(url_for('inicio_fotofrefs'))
    return render_template('upload_frefs.html', form=form)

@app.route('/inicio_fotofrefs')
@login_required
def inicio_fotofrefs():
    lista = []
    for file in listdir(app.root_path+"/static/img/subidas/frefs/"):
        lista.append(file)
    return render_template("inicio_fotofrefs.html", lista=lista)




@app.route('/cert_for4', methods=['GET', 'POST'])
@login_required
def cert_for4():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select fecha_emision_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_emi = cursor.fetchone()
    cursor.execute(
        "select fecha_expiracion_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_exp = cursor.fetchone()
    cursor.execute(
        "select llave_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    llave = cursor.fetchone()
    cursor.execute(
        "select lugar_ins_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    lug = cursor.fetchone()
    cursor.execute(
        "select nom_inspe_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    ins = cursor.fetchone()
    cursor.execute(
        "select * from frefs1 where id_f5 = (select MAX(id) from frefs) ;")
    data = cursor.fetchall()

    return render_template('cert_for4.html', data=data, fec_emi=fec_emi, fec_exp=fec_exp, llave=llave, lug=lug, ins=ins)


@app.route('/genera_pdffrefs')
@login_required
def genera_pdffrefs():
    options = {
        'page-size': 'A4',
        # 'orientation': 'Landscape',
        'margin-top': '20mm',
        'margin-right': '20mm',
        'margin-bottom': '20mm',
        'margin-left': '20mm',
        'encoding': "UTF-8",
        'outline-depth':3,
        # 'footer-center':'[page]',
        'footer-line': None,
        "enable-local-file-access": None,
    }
    path_wkhtmltopdf = r'C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe'
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select fecha_emision_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_emi = cursor.fetchone()
    cursor.execute(
        "select fecha_expiracion_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_exp = cursor.fetchone()
    cursor.execute(
        "select llave_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    llave = cursor.fetchone()
    cursor.execute(
        "select lugar_ins_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    lug = cursor.fetchone()
    cursor.execute(
        "select nom_inspe_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    ins = cursor.fetchone()
    cursor.execute(
        "select * from frefs1 where id_f5 = (select MAX(id) from frefs) ;")
    data = cursor.fetchall()
    html = render_template('cert_for4.html', data=data, fec_emi=fec_emi, fec_exp=fec_exp, llave=llave, lug=lug, ins=ins)
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    #pdfkit.from_file("aplicacion/templates/cert_for1.html", "index.pdf", options=options,configuration=config)
    pdfkit.from_string(html, "cert_for4.pdf", options=options,configuration=config)
    print("="*50)
    return redirect(url_for('inicio'))


@app.route('/home_5', methods=['GET', 'POST'])
@login_required
def home_5():
    cursor = mysql.connection.cursor()
    cursor.execute("select nombre from articulos where id = 8;")
    nom_form = cursor.fetchone()
    cursor.execute("select descripcion from articulos where id = 8;")
    nom_form1 = cursor.fetchone()
    form = datos_reporte()
    if form.validate_on_submit():
        cur = mysql.connection.cursor()
        cur.execute("select (sec+1) from cod_rep where id = 17;")
        sec = cur.fetchone()
        print(sec)
        cur.execute("""
                    UPDATE cod_rep
                    SET sec = %s
                        WHERE id = 17
                """, sec)
        mysql.connection.commit()
        empre = request.form['empresa']
        cur.execute(
            "select CONCAT(prefijo,LPAD(sec, 5, '0')) from cod_rep where id_for = 6;")
        num_rep = cur.fetchone()
        fecha_insp = request.form['fec_inpec']
        fecha_emi = request.form['fec_emision']
        fecha_exp = request.form['fec_expiracion']
        lugar_ins = request.form['lugar_inpec']
        nombre_ins = request.form['nom_inspec']
        cursor = mysql.connection.cursor()
        cursor.execute('insert into formulario (llave_formulario,num_rep,desc_formulario,fecha_inspec_formulario,fecha_emision_formulario,fecha_expiracion_formulario,lugar_ins_formulario,nom_inspe_formulario,empresa,cod_form) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                       (nom_form,num_rep, nom_form1, fecha_insp, fecha_emi, fecha_exp, lugar_ins, nombre_ins, empre,'frgan'))
        mysql.connection.commit()
        flash('Guardado Correctamente')
        datos = cursor.fetchone()
        print(datos)
        # return 'OK'
        return redirect(url_for('frgan'))
    return render_template('home_5.html', form=form, datos=nom_form, desc=nom_form1)


@app.route('/frgan', methods=['GET', 'POST'])
@login_required
def frgan():
    form = formu5()
    if form.validate_on_submit():
        revis = request.form['revis']
        nivel_il = request.form['nivel_il']
        con_sup = request.form['con_sup']
        met_insp = request.form['met_insp']
        tipo_il = request.form['tipo_il']
        check1 = request.form['check1']
        check2 = request.form['check2']
        check3 = request.form['check3']
        detalle = request.form['detalle']
        elem_en = request.form['elem_en']
        revis_p = request.form['revis_p']
        temp_ens = request.form['temp_ens']
        tipo_il_p = request.form['tipo_il_p']
        nivel_il_p = request.form['nivel_il_p']
        mater_base = request.form['mater_base']
        tipo_sec = request.form['tipo_sec']
        equipo = request.form['equipo']
        modelo = request.form['modelo']
        iden = request.form['iden']
        cur = mysql.connection.cursor()
        cur.execute(
            "select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
        llave_form = cur.fetchone()
        cur.execute(
            "select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
        fecha_form = cur.fetchone()
        cur.execute('insert into frgan (id_formulario,fec_formulario,proc,revis,nivel_il,con_sup,met_insp,tipo_il,check1,check2,check3,detalle,elem_en,proc_p,revis_p,temp_ens,tipo_il_p,nivel_il_p,mater_base,tipo_sec,tipo_pen,marca_kit,tiem_pen,met_rem,marca_kit1,tiem_sec,for_rev,marca_kit2,tiem_rev,equipo,modelo,iden) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                    (llave_form, fecha_form, 'PR-INSP-006', revis, nivel_il, con_sup, met_insp, tipo_il, check1, check2, check3, detalle, elem_en, 'PR-INSP-007', revis_p, temp_ens, tipo_il_p, nivel_il_p, mater_base, tipo_sec,'II VISIBLE', 'Met-L-Chek  VP-31A', '5 minutos', 'REMOVIBLE SOLVENTE', 'Met-L-Chek   E-59A', '10 minutos', 'SOLVENTE REMOVED', 'Met-L-Chek   D-70', '10 minutos' , equipo, modelo, iden))
        mysql.connection.commit()
        return redirect(url_for('frgan1'))
    return render_template('frgan.html', form=form)


@app.route('/edit_frgan/<id>', methods=['POST', 'GET'])
@login_required
def get_frgan(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM frgan WHERE id = %s', (id,))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-frgan.html', contact=data[0])


@app.route('/update_frgan/<id>', methods=['POST'])
@login_required
def update_frgan(id):
    if request.method == 'POST':
        proc = request.form['proc']
        revis = request.form['revis']
        nivel_il = request.form['nivel_il']
        con_sup = request.form['con_sup']
        met_insp = request.form['met_insp']
        tipo_il = request.form['tipo_il']
        check1 = request.form['check1']
        check2 = request.form['check2']
        check3 = request.form['check3']
        detalle = request.form['detalle']
        proc_p = request.form['proc_p']
        revis_p = request.form['revis_p']
        temp_ens = request.form['temp_ens']
        tipo_il_p = request.form['tipo_il_p']
        nivel_il_p = request.form['nivel_il_p']
        mater_base = request.form['mater_base']
        tipo_sec = request.form['tipo_sec']
        tipo_pen = request.form['tipo_pen']
        marca_kit = request.form['marca_kit']
        tiem_pen = request.form['tiem_pen']
        met_rem = request.form['met_rem']
        marca_kit1 = request.form['marca_kit1']
        tiem_sec = request.form['tiem_sec']
        for_rev = request.form['for_rev']
        marca_kit2 = request.form['marca_kit2']
        tiem_rev = request.form['tiem_rev']
        equipo = request.form['equipo']
        modelo = request.form['modelo']
        iden = request.form['iden']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE frgan
            SET proc = %s,
                revis = %s,
                nivel_il = %s,
				con_sup = %s,
                met_insp = %s,
				tipo_il = %s,
                check1 = %s,
				check2 = %s,
                check3 = %s,
				detalle = %s,
                proc_p = %s,
				revis_p = %s,
                temp_ens = %s,
				tipo_il_p = %s,
                nivel_il_p = %s,
				mater_base = %s,
                tipo_sec = %s,
				tipo_pen = %s,
                marca_kit = %s,
				tiem_pen = %s,
                met_rem = %s,
				marca_kit1 = %s,
                tiem_sec = %s,
				for_rev = %s,
                marca_kit2 = %s,
				tiem_rev = %s,
                equipo = %s,
				modelo = %s,
                iden = %s
            WHERE id = %s
        """, (proc, revis, nivel_il, con_sup, met_insp, tipo_il, check1, check2, check3, detalle, proc_p, revis_p, temp_ens, tipo_il_p, nivel_il_p, mater_base, tipo_sec, tipo_pen, marca_kit, tiem_pen, met_rem, marca_kit1, tiem_sec, for_rev, marca_kit2, tiem_rev, equipo, modelo, iden, id))
        flash('Contact Updated Successfully')
        mysql.connection.commit()
        return redirect(url_for('resum_frgan'))


@app.route('/add_frgan1', methods=['POST'])
@login_required
def add_frgan():
    form = formu5_5()
    cur = mysql.connection.cursor()
    cur.execute("select (sec+1) from codigo where id_for = 6;")
    sec = cur.fetchone()
    cur.execute("""
            UPDATE codigo
            SET sec = %s
                WHERE id = 6
        """, sec)
    mysql.connection.commit()
    if form.validate_on_submit():
        cur = mysql.connection.cursor()
        ref = request.form['ref']
        cur.execute(
            "select CONCAT(preffijo,LPAD(sec, 4, '0')) from codigo where id_for = 6;")
        cod_enii = cur.fetchone()
        medidas = request.form['medidas']
        capac = request.form['capac']
        asiento = request.form['asiento']
        garganta = request.form['garganta']
        vt = request.form['vt']
        pt = request.form['pt']
        cur.execute(
            "select id from frgan where id = (select MAX(id) from frgan) ;")
        llave_form = cur.fetchone()
        print(cod_enii)
        cur.execute('insert into frgan1 (ref,cod_enii,medidas,capac,asiento,garganta,vt,pt,id_f6) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                    ( ref, cod_enii, medidas, capac, asiento, garganta, vt, pt, llave_form))
        mysql.connection.commit()
        return redirect(url_for('frgan1'))


@app.route('/frgan1', methods=['GET', 'POST'])
@login_required
def frgan1():
    form = formu5_5()
    cur = mysql.connection.cursor()
    cur.execute("select * from frgan1 where id_f6=(select MAX(id) from frgan) ;")
    data = cur.fetchall()
    return render_template('frgan1.html', form=form, data=data)


@app.route('/edit-frgan1/<id>', methods=['POST', 'GET'])
@login_required
def get_frgan1(id):
    cur = mysql.connection.cursor()
    cur.execute(
        'SELECT * FROM frgan1 WHERE num = %s and id_f6=(select MAX(id) from frgan)', [id])
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-frgan1.html', contact=data[0])


@app.route('/update_frgan1/<id>', methods=['POST'])
@login_required
def update_frgan1(id):
    if request.method == 'POST':
        num = request.form['num']
        ref = request.form['ref']
        cod_enii = request.form['cod_enii']
        medidas = request.form['medidas']
        capac = request.form['capac']
        asiento = request.form['asiento']
        garganta = request.form['garganta']
        vt = request.form['vt']
        pt = request.form['pt']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE frgan1
            SET num = %s,
                ref = %s,
                cod_enii = %s,
				medidas = %s,
                capac = %s,
                asiento = %s,
                garganta = %s,
                vt = %s,
				pt = %s
            WHERE num = %s
        """, (num, ref, cod_enii, medidas, capac, asiento, garganta, vt, pt, num))
        flash(' Updated Successfully')
        mysql.connection.commit()
        return redirect(url_for('frgan1'))


@app.route('/resum_frgan')
@login_required
def resum_frgan():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select * from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    datos = cursor.fetchall()
    cursor.execute(
        "select num_rep from formulario where id_formulario = (select MAX(b.id_formulario) from formulario a inner join frgan b on a.id_formulario = b.id_formulario);")
    num_rep = cursor.fetchone()
    cursor.execute(
        "select * from frgan where id_formulario = (select MAX(b.id_formulario) from formulario a inner join frgan b on a.id_formulario = b.id_formulario);")
    datos1 = cursor.fetchall()
    cursor.execute(
        "select MAX(id) from frgan ;")
    data1 = cursor.fetchone()
    cursor.execute(
        "select * from frgan1 where id_f6 = (select MAX(id) from frgan) ;")
    data = cursor.fetchall()
    cursor.execute(
        "select descr from cat_form where codigo = 'FR-INSP-049.04';")
    cata = cursor.fetchone()
    print(data)
    return render_template('resum_frgan.html', datos=datos,num_rep=num_rep, datos1=datos1, contact=data1[0], data=data,cata=cata)

@app.route('/genera_pdffrgan2')
@login_required
def genera_pdffrgan2():
    options = {
        'dpi': '300',
        'page-size': 'A4',
        # 'orientation': 'Landscape',
        'margin-top': '0mm',
        'margin-right': '20mm',
        'margin-bottom': '20mm',
        'margin-left': '10mm',
        'encoding': "UTF-8",
        #'grayscale': None,
        'outline-depth':3,
        # 'footer-center':'[page]',
        'footer-line': None,
        "enable-local-file-access": None,
    }
    path = r'C:/Ricardo/paginas_web/u30/aplicacion/static/css/'
    css = [path + 'style.css']

    path_wkhtmltopdf = r'C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe'
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select llave_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    nom_form = cursor.fetchone()
    cursor.execute(
        "select num_rep from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    num_rep = cursor.fetchone()
    cursor.execute(
        "select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_insp = cursor.fetchone()
    cursor.execute(
        "select fecha_emision_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_emi = cursor.fetchone()
    cursor.execute(
        "select fecha_expiracion_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_exp = cursor.fetchone()
    cursor.execute(
        "select lugar_ins_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    lugar = cursor.fetchone()
    cursor.execute(
        "select nom_inspe_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    inpe = cursor.fetchone()
    cursor.execute(
        "select * from frgan where id_formulario = (select MAX(id_formulario) from formulario);")
    datos1 = cursor.fetchall()
    cursor.execute(
        "select MAX(id) from frgan ;")
    data1 = cursor.fetchone()
    cursor.execute(
        "select * from frgan1 where id_f6 = (select MAX(id) from frgan) ;")
    data = cursor.fetchall()
    html = render_template('resum_frgan_1.html', datos=nom_form,num_rep=num_rep, fec1=fec_insp, fec2=fec_emi, fec3=fec_exp, lugar=lugar, inspector=inpe, datos1=datos1, contact=data1[0], data=data)
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    #pdfkit.from_file("aplicacion/templates/cert_for1.html", "index.pdf", options=options,configuration=config)
    pdfkit.from_string(html, "resum_frgan_1.pdf", options=options,configuration=config)
    #pdfkit.from_url("http://127.0.0.1:5000/cert_for1", "cert_for1.pdf",options=options,configuration=config)
    print("="*50)
    return redirect(url_for('cert_for5'))


@app.route('/reporte_fotofrgan')
@login_required
def reporte_fotofrgan():
    lista = []
    for file in listdir(app.root_path+"/static/img/subidas/frefs/"):
        lista.append(file)
    return render_template("reporte_fotofrgan.html", lista=lista)


@app.route('/upload_frgan', methods=['get', 'post'])
def upload_frgan():
    form = UploadForm()  # carga request.from y request.file
    if form.validate_on_submit():
        f = form.photo.data
        filename = secure_filename(f.filename)
        f.save(app.root_path+"/static/img/subidas/frgan/"+filename)
        foto = app.root_path+"/static/img/subidas/frgan/"+filename
        cursor = mysql.connection.cursor()
        cursor.execute(
            "select id from frgan where id = (select MAX(id) from frgan) ;")
        llave_form = cursor.fetchone()
        cursor.execute('insert into rep_foto_frgan (foto,id_f) VALUES (%s,%s)',
                    ( foto,llave_form))
        mysql.connection.commit()
        return redirect(url_for('inicio_fotofrgan'))
    return render_template('upload_frgan.html', form=form)

@app.route('/inicio_fotofrgan')
@login_required
def inicio_fotofrgan():
    lista = []
    for file in listdir(app.root_path+"/static/img/subidas/frgan/"):
        lista.append(file)
    return render_template("inicio_fotofrgan.html", lista=lista)

@app.route('/cert_for5', methods=['GET', 'POST'])
@login_required
def cert_for5():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select fecha_emision_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_emi = cursor.fetchone()
    cursor.execute(
        "select fecha_expiracion_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_exp = cursor.fetchone()
    cursor.execute(
        "select llave_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    llave = cursor.fetchone()
    cursor.execute(
        "select lugar_ins_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    lug = cursor.fetchone()
    cursor.execute(
        "select nom_inspe_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    ins = cursor.fetchone()
    cursor.execute(
        "select * from frgan1 where id_f6 = (select MAX(id) from frgan) ;")
    data = cursor.fetchall()

    return render_template('cert_for5.html', data=data, fec_emi=fec_emi, fec_exp=fec_exp, llave=llave, lug=lug, ins=ins)



@app.route('/genera_pdffrgan')
@login_required
def genera_pdffrgan():
    options = {
        'page-size': 'A4',
        # 'orientation': 'Landscape',
        'margin-top': '20mm',
        'margin-right': '20mm',
        'margin-bottom': '20mm',
        'margin-left': '20mm',
        'encoding': "UTF-8",
        'outline-depth':3,
        # 'footer-center':'[page]',
        'footer-line': None,
        "enable-local-file-access": None,
    }
    path_wkhtmltopdf = r'C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe'
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select fecha_emision_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_emi = cursor.fetchone()
    cursor.execute(
        "select fecha_expiracion_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_exp = cursor.fetchone()
    cursor.execute(
        "select llave_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    llave = cursor.fetchone()
    cursor.execute(
        "select lugar_ins_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    lug = cursor.fetchone()
    cursor.execute(
        "select nom_inspe_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    ins = cursor.fetchone()
    cursor.execute(
        "select * from frgan1 where id_f6 = (select MAX(id) from frgan) ;")
    data = cursor.fetchall()
    html = render_template('cert_for5.html', data=data, fec_emi=fec_emi, fec_exp=fec_exp, llave=llave, lug=lug, ins=ins)
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    #pdfkit.from_file("aplicacion/templates/cert_for1.html", "index.pdf", options=options,configuration=config)
    pdfkit.from_string(html, "cert_for5.pdf", options=options,configuration=config)
    print("="*50)
    return redirect(url_for('inicio'))



@app.route('/home_6', methods=['GET', 'POST'])
@login_required
def home_6():
    cursor = mysql.connection.cursor()
    cursor.execute("select nombre from articulos where id =9;")
    nom_form = cursor.fetchone()
    cursor.execute("select descripcion from articulos where id = 9;")
    nom_form1 = cursor.fetchone()
    form = datos_reporte()
    if form.validate_on_submit():
        cur = mysql.connection.cursor()
        cur.execute("select (sec+1) from cod_rep where id = 18;")
        sec = cur.fetchone()
        print(sec)
        cur.execute("""
                    UPDATE cod_rep
                    SET sec = %s
                        WHERE id = 18
                """, sec)
        mysql.connection.commit()
        empre = request.form['empresa']
        cur.execute(
            "select CONCAT(prefijo,LPAD(sec, 5, '0')) from cod_rep where id_for = 7;")
        num_rep = cur.fetchone()
        fecha_insp = request.form['fec_inpec']
        fecha_emi = request.form['fec_emision']
        fecha_exp = request.form['fec_expiracion']
        lugar_ins = request.form['lugar_inpec']
        nombre_ins = request.form['nom_inspec']
        cursor = mysql.connection.cursor()
        cursor.execute('insert into formulario (llave_formulario,num_rep,desc_formulario,fecha_inspec_formulario,fecha_emision_formulario,fecha_expiracion_formulario,lugar_ins_formulario,nom_inspe_formulario,empresa,cod_form) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                       (nom_form,num_rep, nom_form1, fecha_insp, fecha_emi, fecha_exp, lugar_ins, nombre_ins, empre,'frgri'))
        mysql.connection.commit()
        flash('Guardado Correctamente')
        datos = cursor.fetchone()
        print(datos)
        # return 'OK'
        return redirect(url_for('frgri'))
    return render_template('home_6.html', form=form, datos=nom_form, desc=nom_form1)


@app.route('/frgri', methods=['GET', 'POST'])
@login_required
def frgri():
    form = formu6()
    if form.validate_on_submit():
        revis = request.form['revis']
        nivel_il = request.form['nivel_il']
        con_sup = request.form['con_sup']
        met_insp = request.form['met_insp']
        tipo_il = request.form['tipo_il']
        check1 = request.form['check1']
        check2 = request.form['check2']
        check3 = request.form['check3']
        detalle = request.form['detalle']
        elem_en = request.form['elem_en']
        revis_p = request.form['revis_p']
        temp_ens = request.form['temp_ens']
        tipo_il_p = request.form['tipo_il_p']
        nivel_il_p = request.form['nivel_il_p']
        mater_base = request.form['mater_base']
        tipo_sec = request.form['tipo_sec']
        equipo = request.form['equipo']
        modelo = request.form['modelo']
        iden = request.form['iden']
        cur = mysql.connection.cursor()
        cur.execute(
            "select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
        llave_form = cur.fetchone()
        cur.execute(
            "select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
        fecha_form = cur.fetchone()
        cur.execute('insert into frgri (id_formulario,fec_formulario,proc,revis,nivel_il,con_sup,met_insp,tipo_il,check1,check2,check3,detalle,elem_en,proc_p,revis_p,temp_ens,tipo_il_p,nivel_il_p,mater_base,tipo_sec,tipo_pen,marca_kit,tiem_pen,met_rem,marca_kit1,tiem_sec,for_rev,marca_kit2,tiem_rev,equipo,modelo,iden) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                    (llave_form, fecha_form, 'PR-INSP-006', revis, nivel_il, con_sup, met_insp, tipo_il, check1, check2, check3, detalle, elem_en, 'PR-INSP-007', revis_p, temp_ens, tipo_il_p, nivel_il_p, mater_base, tipo_sec,  'II VISIBLE', 'Met-L-Chek  VP-31A', '5 minutos', 'REMOVIBLE SOLVENTE', 'Met-L-Chek   E-59A', '10 minutos', 'SOLVENTE REMOVED', 'Met-L-Chek   D-70', '10 minutos',  equipo, modelo, iden))
        mysql.connection.commit()
        return redirect(url_for('frgri1'))
    return render_template('frgri.html', form=form)


@app.route('/edit_frgri/<id>', methods=['POST', 'GET'])
@login_required
def get_frgri(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM frgri WHERE id = %s', (id,))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-frgri.html', contact=data[0])


@app.route('/update_frgri/<id>', methods=['POST'])
@login_required
def update_frgri(id):
    if request.method == 'POST':
        proc = request.form['proc']
        revis = request.form['revis']
        nivel_il = request.form['nivel_il']
        con_sup = request.form['con_sup']
        met_insp = request.form['met_insp']
        tipo_il = request.form['tipo_il']
        check1 = request.form['check1']
        check2 = request.form['check2']
        check3 = request.form['check3']
        detalle = request.form['detalle']
        proc_p = request.form['proc_p']
        revis_p = request.form['revis_p']
        temp_ens = request.form['temp_ens']
        tipo_il_p = request.form['tipo_il_p']
        nivel_il_p = request.form['nivel_il_p']
        mater_base = request.form['mater_base']
        tipo_sec = request.form['tipo_sec']
        tipo_pen = request.form['tipo_pen']
        marca_kit = request.form['marca_kit']
        tiem_pen = request.form['tiem_pen']
        met_rem = request.form['met_rem']
        marca_kit1 = request.form['marca_kit1']
        tiem_sec = request.form['tiem_sec']
        for_rev = request.form['for_rev']
        marca_kit2 = request.form['marca_kit2']
        tiem_rev = request.form['tiem_rev']
        equipo = request.form['equipo']
        modelo = request.form['modelo']
        iden = request.form['iden']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE frgri
            SET proc = %s,
                revis = %s,
                nivel_il = %s,
				con_sup = %s,
                met_insp = %s,
				tipo_il = %s,
                check1 = %s,
				check2 = %s,
                check3 = %s,
				detalle = %s,
                proc_p = %s,
				revis_p = %s,
                temp_ens = %s,
				tipo_il_p = %s,
                nivel_il_p = %s,
				mater_base = %s,
                tipo_sec = %s,
				tipo_pen = %s,
                marca_kit = %s,
				tiem_pen = %s,
                met_rem = %s,
				marca_kit1 = %s,
                tiem_sec = %s,
				for_rev = %s,
                marca_kit2 = %s,
				tiem_rev = %s,
                equipo = %s,
				modelo = %s,
                iden = %s
            WHERE id = %s
        """, (proc, revis, nivel_il, con_sup, met_insp, tipo_il, check1, check2, check3, detalle, proc_p, revis_p, temp_ens, tipo_il_p, nivel_il_p, mater_base, tipo_sec, tipo_pen, marca_kit, tiem_pen, met_rem, marca_kit1, tiem_sec, for_rev, marca_kit2, tiem_rev, equipo, modelo, iden, id))
        flash('Contact Updated Successfully')
        mysql.connection.commit()
        return redirect(url_for('resum_frgri'))


@app.route('/add_frgri1', methods=['POST'])
@login_required
def add_frgri():
    form = formu6_6()
    cur = mysql.connection.cursor()
    cur.execute("select (sec+1) from codigo where id_for = 7;")
    sec = cur.fetchone()
    cur.execute("""
            UPDATE codigo
            SET sec = %s
                WHERE id = 7
        """, sec)
    mysql.connection.commit()
    if form.validate_on_submit():
        cur = mysql.connection.cursor()
        ref = request.form['ref']
        cur.execute(
            "select CONCAT(preffijo,LPAD(sec, 4, '0')) from codigo where id_for = 7;")
        cod_enii = cur.fetchone()
        medidas = request.form['medidas']
        capac = request.form['capac']
        diam_cue = request.form['diam_cue']
        vt = request.form['vt']
        pt = request.form['pt']
        cur.execute(
            "select id from frgri where id = (select MAX(id) from frgri) ;")
        llave_form = cur.fetchone()
        print(cod_enii)
        cur.execute('insert into frgri1 (ref,cod_enii,medidas,capac,diam_cue,vt,pt,id_f7) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',
                    ( ref, cod_enii, medidas, capac, diam_cue, vt, pt, llave_form))
        mysql.connection.commit()
        return redirect(url_for('frgri1'))


@app.route('/frgri1', methods=['GET', 'POST'])
@login_required
def frgri1():
    form = formu6_6()
    cur = mysql.connection.cursor()
    cur.execute("select * from frgri1 where id_f7=(select MAX(id) from frgri) ;")
    data = cur.fetchall()
    return render_template('frgri1.html', form=form, data=data)


@app.route('/edit-frgri1/<id>', methods=['POST', 'GET'])
@login_required
def get_frgri1(id):
    cur = mysql.connection.cursor()
    cur.execute(
        'SELECT * FROM frgri1 WHERE num = %s and id_f7=(select MAX(id) from frgri)', [id])
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-frgri1.html', contact=data[0])


@app.route('/update_frgri1/<id>', methods=['POST'])
@login_required
def update_frgri1(id):
    if request.method == 'POST':
        num = request.form['num']
        ref = request.form['ref']
        cod_enii = request.form['cod_enii']
        medidas = request.form['medidas']
        capac = request.form['capac']
        diam_cue = request.form['diam_cue']
        vt = request.form['vt']
        pt = request.form['pt']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE frgri1
            SET num = %s,
                ref = %s,
                cod_enii = %s,
				medidas = %s,
                capac = %s,
                diam_cue = %s,
                vt = %s,
				pt = %s
            WHERE num = %s
        """, (num, ref, cod_enii, medidas, capac, diam_cue, vt, pt, num))
        flash(' Updated Successfully')
        mysql.connection.commit()
        return redirect(url_for('frgri1'))


@app.route('/resum_frgri')
@login_required
def resum_frgri():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select * from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    datos = cursor.fetchall()
    cursor.execute(
        "select num_rep from formulario where id_formulario = (select MAX(b.id_formulario) from formulario a inner join frgri b on a.id_formulario = b.id_formulario);")
    num_rep = cursor.fetchone()
    cursor.execute(
        "select * from frgri where id_formulario = (select MAX(b.id_formulario) from formulario a inner join frgri b on a.id_formulario = b.id_formulario);")
    datos1 = cursor.fetchall()
    cursor.execute(
        "select MAX(id) from frgri ;")
    data1 = cursor.fetchone()
    cursor.execute(
        "select * from frgri1 where id_f7 = (select MAX(id) from frgri) ;")
    data = cursor.fetchall()
    cursor.execute(
        "select descr from cat_form where codigo = 'FR-INSP-051.03';")
    cata = cursor.fetchone()
    print(data)
    return render_template('resum_frgri.html', datos=datos,num_rep=num_rep,datos1=datos1, contact=data1[0], data=data,cata=cata)

@app.route('/genera_pdffrgri2')
@login_required
def genera_pdffrgri2():
    options = {
        'dpi': '300',
        'page-size': 'A4',
        # 'orientation': 'Landscape',
        'margin-top': '0mm',
        'margin-right': '20mm',
        'margin-bottom': '20mm',
        'margin-left': '10mm',
        'encoding': "UTF-8",
        #'grayscale': None,
        'outline-depth':3,
        # 'footer-center':'[page]',
        'footer-line': None,
        "enable-local-file-access": None,
    }
    path = r'C:/Ricardo/paginas_web/u30/aplicacion/static/css/'
    css = [path + 'style.css']

    path_wkhtmltopdf = r'C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe'
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select llave_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    nom_form = cursor.fetchone()
    cursor.execute(
        "select num_rep from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    num_rep = cursor.fetchone()
    cursor.execute(
        "select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_insp = cursor.fetchone()
    cursor.execute(
        "select fecha_emision_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_emi = cursor.fetchone()
    cursor.execute(
        "select fecha_expiracion_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_exp = cursor.fetchone()
    cursor.execute(
        "select lugar_ins_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    lugar = cursor.fetchone()
    cursor.execute(
        "select nom_inspe_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    inpe = cursor.fetchone()
    cursor.execute(
        "select * from frgri where id_formulario = (select MAX(id_formulario) from formulario);")
    datos1 = cursor.fetchall()
    cursor.execute(
        "select MAX(id) from frgri ;")
    data1 = cursor.fetchone()
    cursor.execute(
        "select * from frgri1 where id_f7 = (select MAX(id) from frgri) ;")
    data = cursor.fetchall()
    html = render_template('resum_frgri_1.html', datos=nom_form,num_rep=num_rep, fec1=fec_insp, fec2=fec_emi, fec3=fec_exp, lugar=lugar, inspector=inpe, datos1=datos1, contact=data1[0], data=data)
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    #pdfkit.from_file("aplicacion/templates/cert_for1.html", "index.pdf", options=options,configuration=config)
    pdfkit.from_string(html, "resum_frgri_1.pdf", options=options,configuration=config)
    #pdfkit.from_url("http://127.0.0.1:5000/cert_for1", "cert_for1.pdf",options=options,configuration=config)
    print("="*50)
    return redirect(url_for('cert_for6'))

@app.route('/reporte_fotofrgri')
@login_required
def reporte_fotofrgri():
    lista = []
    for file in listdir(app.root_path+"/static/img/subidas/frgri/"):
        lista.append(file)
    return render_template("reporte_fotofrgri.html", lista=lista)


@app.route('/upload_frgri', methods=['get', 'post'])
def upload_frgri():
    form = UploadForm()  # carga request.from y request.file
    if form.validate_on_submit():
        f = form.photo.data
        filename = secure_filename(f.filename)
        f.save(app.root_path+"/static/img/subidas/frgri/"+filename)
        foto = app.root_path+"/static/img/subidas/frgri/"+filename
        cursor = mysql.connection.cursor()
        cursor.execute(
            "select id from frgri where id = (select MAX(id) from frgri) ;")
        llave_form = cursor.fetchone()
        cursor.execute('insert into rep_foto_frgri (foto,id_f) VALUES (%s,%s)',
                    ( foto,llave_form))
        mysql.connection.commit()
        return redirect(url_for('inicio_fotofrgri'))
    return render_template('upload_frgri.html', form=form)

@app.route('/inicio_fotofrgri')
@login_required
def inicio_fotofrgri():
    lista = []
    for file in listdir(app.root_path+"/static/img/subidas/frgri/"):
        lista.append(file)
    return render_template("inicio_fotofrgri.html", lista=lista)



@app.route('/cert_for6', methods=['GET', 'POST'])
@login_required
def cert_for6():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select fecha_emision_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_emi = cursor.fetchone()
    cursor.execute(
        "select fecha_expiracion_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_exp = cursor.fetchone()
    cursor.execute(
        "select llave_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    llave = cursor.fetchone()
    cursor.execute(
        "select lugar_ins_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    lug = cursor.fetchone()
    cursor.execute(
        "select nom_inspe_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    ins = cursor.fetchone()
    cursor.execute(
        "select * from frgri1 where id_f7 = (select MAX(id) from frgri) ;")
    data = cursor.fetchall()

    return render_template('cert_for6.html', data=data, fec_emi=fec_emi, fec_exp=fec_exp, llave=llave, lug=lug, ins=ins)

@app.route('/genera_pdffrgri')
@login_required
def genera_pdffrgri():
    options = {
        'page-size': 'A4',
        # 'orientation': 'Landscape',
        'margin-top': '20mm',
        'margin-right': '20mm',
        'margin-bottom': '20mm',
        'margin-left': '20mm',
        'encoding': "UTF-8",
        'outline-depth':3,
        # 'footer-center':'[page]',
        'footer-line': None,
        "enable-local-file-access": None,
    }
    path_wkhtmltopdf = r'C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe'
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select fecha_emision_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_emi = cursor.fetchone()
    cursor.execute(
        "select fecha_expiracion_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_exp = cursor.fetchone()
    cursor.execute(
        "select llave_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    llave = cursor.fetchone()
    cursor.execute(
        "select lugar_ins_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    lug = cursor.fetchone()
    cursor.execute(
        "select nom_inspe_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    ins = cursor.fetchone()
    cursor.execute(
        "select * from frgri1 where id_f7 = (select MAX(id) from frgri) ;")
    data = cursor.fetchall()
    html = render_template('cert_for6.html', data=data, fec_emi=fec_emi, fec_exp=fec_exp, llave=llave, lug=lug, ins=ins)
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    #pdfkit.from_file("aplicacion/templates/cert_for1.html", "index.pdf", options=options,configuration=config)
    pdfkit.from_string(html, "cert_for6.pdf", options=options,configuration=config)
    print("="*50)
    return redirect(url_for('inicio'))


@app.route('/home_7', methods=['GET', 'POST'])
@login_required
def home_7():
    cursor = mysql.connection.cursor()
    cursor.execute("select nombre from articulos where id =11;")
    nom_form = cursor.fetchone()
    cursor.execute("select descripcion from articulos where id = 11;")
    nom_form1 = cursor.fetchone()
    form = datos_reporte()
    if form.validate_on_submit():
        cur = mysql.connection.cursor()
        cur.execute("select (sec+1) from cod_rep where id = 19;")
        sec = cur.fetchone()
        print(sec)
        cur.execute("""
                    UPDATE cod_rep
                    SET sec = %s
                        WHERE id = 19
                """, sec)
        mysql.connection.commit()
        empre = request.form['empresa']
        cur.execute(
            "select CONCAT(prefijo,LPAD(sec, 5, '0')) from cod_rep where id_for = 8;")
        num_rep = cur.fetchone()
        fecha_insp = request.form['fec_inpec']
        fecha_emi = request.form['fec_emision']
        fecha_exp = request.form['fec_expiracion']
        lugar_ins = request.form['lugar_inpec']
        nombre_ins = request.form['nom_inspec']
        cursor = mysql.connection.cursor()
        cursor.execute('insert into formulario (llave_formulario,num_rep,desc_formulario,fecha_inspec_formulario,fecha_emision_formulario,fecha_expiracion_formulario,lugar_ins_formulario,nom_inspe_formulario,empresa,cod_form) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                       (nom_form,num_rep, nom_form1, fecha_insp, fecha_emi, fecha_exp, lugar_ins, nombre_ins, empre,'frkpi'))
        mysql.connection.commit()
        flash('Guardado Correctamente')
        datos = cursor.fetchone()
        print(datos)
        # return 'OK'
        return redirect(url_for('frkpi'))
    return render_template('home_7.html', form=form, datos=nom_form, desc=nom_form1)


@app.route('/frkpi', methods=['GET', 'POST'])
@login_required
def frkpi():
    form = formu7()
    if form.validate_on_submit():
        revis = request.form['revis']
        nivel_il = request.form['nivel_il']
        con_sup = request.form['con_sup']
        met_insp = request.form['met_insp']
        tipo_il = request.form['tipo_il']
        check1 = request.form['check1']
        check2 = request.form['check2']
        check3 = request.form['check3']
        detalle = request.form['detalle']
        elem_en = request.form['elem_en']
        revis_p = request.form['revis_p']
        temp_ens = request.form['temp_ens']
        tipo_il_p = request.form['tipo_il_p']
        nivel_il_p = request.form['nivel_il_p']
        mater_base = request.form['mater_base']
        tipo_sec = request.form['tipo_sec']
        equipo = request.form['equipo']
        marca = request.form['marca']
        iden = request.form['iden']
        marca_pk = request.form['marca_pk']
        iden_pk = request.form['iden_pk']
        modelo_pk = request.form['modelo_pk']
        capac_pk = request.form['capac_pk']
        dia_sup = request.form['dia_sup']
        dia_cen = request.form['dia_cen']
        dia_inf = request.form['dia_inf']
        obs = request.form['obs']
        vt = request.form['vt']
        pt = request.form['pt']
        cur = mysql.connection.cursor()
        cur.execute(
            "select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
        llave_form = cur.fetchone()
        cur.execute(
            "select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
        fecha_form = cur.fetchone()
        cur.execute('insert into frkpi (id_formulario,fec_formulario,proc,revis,nivel_il,con_sup,met_insp,tipo_il,check1,check2,check3,detalle,elem_en,proc_p,revis_p,temp_ens,tipo_il_p,nivel_il_p,mater_base,tipo_sec,marca_pk,iden_pk,modelo_pk,vt,pt,tipo_pen,marca_kit,tiem_pen,met_rem,marca_kit1,tiem_sec,for_rev,marca_kit2,tiem_rev,equipo,marca,iden,capac_pk,dia_sup,dia_cen,dia_inf,obs) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                    (llave_form, fecha_form, 'PR-INSP-006', revis, nivel_il, con_sup, met_insp, tipo_il, check1, check2, check3, detalle, elem_en, 'PR-INSP-007', revis_p, temp_ens, tipo_il_p, nivel_il_p, mater_base, tipo_sec, marca_pk, iden_pk, modelo_pk, vt, pt, 'II VISIBLE', 'Met-L-Chek  VP-31A', '5 minutos', 'REMOVIBLE SOLVENTE', 'Met-L-Chek   E-59A', '10 minutos', 'SOLVENTE REMOVED', 'Met-L-Chek   D-70', '10 minutos', equipo, marca, capac_pk, iden, dia_sup, dia_cen, dia_inf, obs))
        mysql.connection.commit()
        return redirect(url_for('resum_frkpi'))
    return render_template('frkpi.html', form=form)



@app.route('/edit_frkpi/<id>', methods=['POST', 'GET'])
@login_required
def get_frkpi(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM frkpi WHERE id = %s', (id,))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-frkpi.html', contact=data[0])



@app.route('/update_frkpi/<id>', methods=['POST'])
@login_required
def update_frkpi(id):
    if request.method == 'POST':
        proc = request.form['proc']
        revis = request.form['revis']
        nivel_il = request.form['nivel_il']
        con_sup = request.form['con_sup']
        met_insp = request.form['met_insp']
        tipo_il = request.form['tipo_il']
        check1 = request.form['check1']
        check2 = request.form['check2']
        check3 = request.form['check3']
        detalle = request.form['detalle']
        proc_p = request.form['proc_p']
        revis_p = request.form['revis_p']
        temp_ens = request.form['temp_ens']
        tipo_il_p = request.form['tipo_il_p']
        nivel_il_p = request.form['nivel_il_p']
        mater_base = request.form['mater_base']
        tipo_sec = request.form['tipo_sec']
        tipo_pen = request.form['tipo_pen']
        marca_kit = request.form['marca_kit']
        tiem_pen = request.form['tiem_pen']
        met_rem = request.form['met_rem']
        marca_kit1 = request.form['marca_kit1']
        tiem_sec = request.form['tiem_sec']
        for_rev = request.form['for_rev']
        marca_kit2 = request.form['marca_kit2']
        tiem_rev = request.form['tiem_rev']
        equipo = request.form['equipo']
        marca = request.form['marca']
        iden = request.form['iden']
        marca_pk = request.form['marca_pk']
        iden_pk = request.form['iden_pk']
        modelo_pk = request.form['modelo_pk']
        capac_pk = request.form['capac_pk']
        dia_sup = request.form['dia_sup']
        dia_cen = request.form['dia_cen']
        dia_inf = request.form['dia_inf']
        obs = request.form['obs']
        vt = request.form['vt']
        pt = request.form['pt']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE frkpi
            SET proc = %s,
                revis = %s,
                nivel_il = %s,
				con_sup = %s,
                met_insp = %s,
				tipo_il = %s,
                check1 = %s,
				check2 = %s,
                check3 = %s,
				detalle = %s,
                proc_p = %s,
				revis_p = %s,
                temp_ens = %s,
				tipo_il_p = %s,
                nivel_il_p = %s,
				mater_base = %s,
                tipo_sec = %s,
				tipo_pen = %s,
                marca_kit = %s,
				tiem_pen = %s,
                met_rem = %s,
				marca_kit1 = %s,
                tiem_sec = %s,
				for_rev = %s,
                marca_kit2 = %s,
				tiem_rev = %s,
                equipo = %s,
				marca = %s,
                iden = %s,
                marca_pk = %s,
                iden_pk = %s,
                modelo_pk = %s,
                capac_pk = %s,
                dia_sup = %s,
                dia_cen = %s,
                dia_inf = %s,
                obs = %s,
                vt = %s,
                pt = %s
            WHERE id = %s
        """, (proc, revis, nivel_il, con_sup, met_insp, tipo_il, check1, check2, check3, detalle, proc_p, revis_p, temp_ens, tipo_il_p, nivel_il_p, mater_base, tipo_sec, tipo_pen, marca_kit, tiem_pen, met_rem, marca_kit1, tiem_sec, for_rev, marca_kit2, tiem_rev, equipo, marca, iden, marca_pk, iden_pk, modelo_pk, capac_pk,dia_sup, dia_cen,dia_inf,obs,vt,pt,id))
        flash('Contact Updated Successfully')
        mysql.connection.commit()
        return redirect(url_for('resum_frkpi'))


@app.route('/resum_frkpi')
@login_required
def resum_frkpi():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select * from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    datos = cursor.fetchall()
    cursor.execute(
        "select num_rep from formulario where id_formulario = (select MAX(b.id_formulario) from formulario a inner join frkpi b on a.id_formulario = b.id_formulario);")
    num_rep = cursor.fetchone()
    cursor.execute(
        "select * from frkpi where id_formulario = (select MAX(b.id_formulario) from formulario a inner join frkpi b on a.id_formulario = b.id_formulario);")
    datos1 = cursor.fetchall()
    cursor.execute(
        "select MAX(id) from frkpi ;")
    data1 = cursor.fetchone()
    cursor.execute(
        "select descr from cat_form where codigo = 'FR-INSP-053.04';")
    cata = cursor.fetchone()
    
    print(data1)
    
    return render_template('resum_frkpi.html', datos=datos,num_rep=num_rep, datos1=datos1, contact=data1[0],cata=cata)


@app.route('/genera_pdfrkpif2')
@login_required
def genera_pdffrkpi2():
    options = {
        'dpi': '300',
        'page-size': 'A4',
        # 'orientation': 'Landscape',
        'margin-top': '0mm',
        'margin-right': '20mm',
        'margin-bottom': '20mm',
        'margin-left': '10mm',
        'encoding': "UTF-8",
        #'grayscale': None,
        'outline-depth':3,
        # 'footer-center':'[page]',
        'footer-line': None,
        "enable-local-file-access": None,
    }
    path = r'C:/Ricardo/paginas_web/u30/aplicacion/static/css/'
    css = [path + 'style.css']

    path_wkhtmltopdf = r'C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe'
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select llave_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    nom_form = cursor.fetchone()
    cursor.execute(
        "select num_rep from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    num_rep = cursor.fetchone()
    cursor.execute(
        "select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_insp = cursor.fetchone()
    cursor.execute(
        "select fecha_emision_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_emi = cursor.fetchone()
    cursor.execute(
        "select fecha_expiracion_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_exp = cursor.fetchone()
    cursor.execute(
        "select lugar_ins_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    lugar = cursor.fetchone()
    cursor.execute(
        "select nom_inspe_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    inpe = cursor.fetchone()
    cursor.execute(
        "select * from frkpi where id_formulario = (select MAX(id_formulario) from formulario);")
    datos1 = cursor.fetchall()
    cursor.execute(
        "select MAX(id) from frkpi ;")
    data1 = cursor.fetchone()
    html = render_template('resum_frkpi_1.html', datos=nom_form,num_rep=num_rep, fec1=fec_insp, fec2=fec_emi, fec3=fec_exp, lugar=lugar, inspector=inpe, datos1=datos1, contact=data1[0])
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    #pdfkit.from_file("aplicacion/templates/cert_for1.html", "index.pdf", options=options,configuration=config)
    pdfkit.from_string(html, "resum_frkpi_1.pdf", options=options,configuration=config)
    #pdfkit.from_url("http://127.0.0.1:5000/cert_for1", "cert_for1.pdf",options=options,configuration=config)
    print("="*50)
    return redirect(url_for('cert_for7'))

@app.route('/reporte_fotofrkpi')
@login_required
def reporte_fotofrkpi():
    lista = []
    for file in listdir(app.root_path+"/static/img/subidas/frkpi/"):
        lista.append(file)
    return render_template("reporte_fotofrkpi.html", lista=lista)


@app.route('/upload_frkpi', methods=['get', 'post'])
def upload_frkpi():
    form = UploadForm()  # carga request.from y request.file
    if form.validate_on_submit():
        f = form.photo.data
        filename = secure_filename(f.filename)
        f.save(app.root_path+"/static/img/subidas/frkpi/"+filename)
        foto = app.root_path+"/static/img/subidas/frkpi/"+filename
        cursor = mysql.connection.cursor()
        cursor.execute(
            "select id from frkpi where id = (select MAX(id) from frkpi) ;")
        llave_form = cursor.fetchone()
        cursor.execute('insert into rep_foto_frkpi (foto,id_f) VALUES (%s,%s)',
                    ( foto,llave_form))
        mysql.connection.commit()
        return redirect(url_for('inicio_fotofrkpi'))
    return render_template('upload_frkpi.html', form=form)

@app.route('/inicio_fotofrkpi')
@login_required
def inicio_fotofrkpi():
    lista = []
    for file in listdir(app.root_path+"/static/img/subidas/frkpi/"):
        lista.append(file)
    return render_template("inicio_fotofrkpi.html", lista=lista)


@app.route('/cert_for7', methods=['GET', 'POST'])
@login_required
def cert_for7():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select marca_pk from frkpi where id_formulario = (select MAX(id_formulario) from formulario);")
    marca_pk = cursor.fetchone()
    cursor.execute(
        "select modelo_pk from frkpi where id_formulario = (select MAX(id_formulario) from formulario);")
    modelo_pk = cursor.fetchone()
    cursor.execute(
        "select iden_pk from frkpi where id_formulario = (select MAX(id_formulario) from formulario);")
    iden_pk = cursor.fetchone()
    cursor.execute(
        "select capac_pk from frkpi where id_formulario = (select MAX(id_formulario) from formulario);")
    capac_pk = cursor.fetchone()
    cursor.execute(
        "select fecha_emision_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_emi = cursor.fetchone()
    cursor.execute(
        "select fecha_expiracion_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_exp = cursor.fetchone()
    return render_template('cert_for7.html', marca_pk=marca_pk, modelo_pk=modelo_pk, iden_pk=iden_pk, capac_pk=capac_pk, fec_emi=fec_emi, fec_exp=fec_exp)



@app.route('/genera_pdffrkpi')
@login_required
def genera_pdffrkpi():
    options = {
        'page-size': 'A4',
        # 'orientation': 'Landscape',
        'margin-top': '20mm',
        'margin-right': '20mm',
        'margin-bottom': '20mm',
        'margin-left': '20mm',
        'encoding': "UTF-8",
        'outline-depth':3,
        # 'footer-center':'[page]',
        'footer-line': None,
        "enable-local-file-access": None,
    }
    path_wkhtmltopdf = r'C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe'
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select marca_pk from frkpi where id_formulario = (select MAX(id_formulario) from formulario);")
    marca_pk = cursor.fetchone()
    cursor.execute(
        "select modelo_pk from frkpi where id_formulario = (select MAX(id_formulario) from formulario);")
    modelo_pk = cursor.fetchone()
    cursor.execute(
        "select iden_pk from frkpi where id_formulario = (select MAX(id_formulario) from formulario);")
    iden_pk = cursor.fetchone()
    cursor.execute(
        "select capac_pk from frkpi where id_formulario = (select MAX(id_formulario) from formulario);")
    capac_pk = cursor.fetchone()
    cursor.execute(
        "select fecha_emision_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_emi = cursor.fetchone()
    cursor.execute(
        "select fecha_expiracion_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_exp = cursor.fetchone()
    html = render_template('cert_for7.html', marca_pk=marca_pk, modelo_pk=modelo_pk, iden_pk=iden_pk, capac_pk=capac_pk, fec_emi=fec_emi, fec_exp=fec_exp)
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    #pdfkit.from_file("aplicacion/templates/cert_for1.html", "index.pdf", options=options,configuration=config)
    pdfkit.from_string(html, "cert_for7.pdf", options=options,configuration=config)
    print("="*50)
    return redirect(url_for('inicio'))


@app.route('/home_8', methods=['GET', 'POST'])
@login_required
def home_8():
    cursor = mysql.connection.cursor()
    cursor.execute("select nombre from articulos where id =12;")
    nom_form = cursor.fetchone()
    cursor.execute("select descripcion from articulos where id = 12;")
    nom_form1 = cursor.fetchone()
    form = datos_reporte()
    if form.validate_on_submit():
        cur = mysql.connection.cursor()
        cur.execute("select (sec+1) from cod_rep where id = 20;")
        sec = cur.fetchone()
        print(sec)
        cur.execute("""
                    UPDATE cod_rep
                    SET sec = %s
                        WHERE id = 20
                """, sec)
        mysql.connection.commit()
        empre = request.form['empresa']
        cur.execute(
            "select CONCAT(prefijo,LPAD(sec, 5, '0')) from cod_rep where id_for = 9;")
        num_rep = cur.fetchone()
        fecha_insp = request.form['fec_inpec']
        fecha_emi = request.form['fec_emision']
        fecha_exp = request.form['fec_expiracion']
        lugar_ins = request.form['lugar_inpec']
        nombre_ins = request.form['nom_inspec']
        cursor = mysql.connection.cursor()
        cursor.execute('insert into formulario (llave_formulario,num_rep,desc_formulario,fecha_inspec_formulario,fecha_emision_formulario,fecha_expiracion_formulario,lugar_ins_formulario,nom_inspe_formulario,empresa,cod_form) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                       (nom_form,num_rep, nom_form1, fecha_insp, fecha_emi, fecha_exp, lugar_ins, nombre_ins, empre,'frqru'))
        mysql.connection.commit()
        flash('Guardado Correctamente')
        datos = cursor.fetchone()
        print(datos)
        # return 'OK'
        return redirect(url_for('frqru'))
    return render_template('home_8.html', form=form, datos=nom_form, desc=nom_form1)


@app.route('/frqru', methods=['GET', 'POST'])
@login_required
def frqru():
    form = formu8()
    if form.validate_on_submit():
        revis = request.form['revis']
        nivel_il = request.form['nivel_il']
        con_sup = request.form['con_sup']
        met_insp = request.form['met_insp']
        tipo_il = request.form['tipo_il']
        check1 = request.form['check1']
        check2 = request.form['check2']
        check3 = request.form['check3']
        detalle = request.form['detalle']
        revis_p = request.form['revis_p']
        temp_ens = request.form['temp_ens']
        tipo_il_p = request.form['tipo_il_p']
        nivel_il_p = request.form['nivel_il_p']
        mater_base = request.form['mater_base']
        tipo_sec = request.form['tipo_sec']
        equipo = request.form['equipo']
        marca = request.form['marca']
        iden = request.form['iden']
        marca_pk = request.form['marca_pk']
        iden_pk = request.form['iden_pk']
        modelo_pk = request.form['modelo_pk']
        capac_pk = request.form['capac_pk']
        obs = request.form['obs']
        vt = request.form['vt']
        pt = request.form['pt']
        cur = mysql.connection.cursor()
        cur.execute(
            "select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
        llave_form = cur.fetchone()
        cur.execute(
            "select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
        fecha_form = cur.fetchone()
        cur.execute('insert into frqru (id_formulario,fec_formulario,proc,revis,nivel_il,con_sup,met_insp,tipo_il,check1,check2,check3,detalle,proc_p,revis_p,temp_ens,tipo_il_p,nivel_il_p,mater_base,tipo_sec,marca_pk,iden_pk,modelo_pk,vt,pt,tipo_pen,marca_kit,tiem_pen,met_rem,marca_kit1,tiem_sec,for_rev,marca_kit2,tiem_rev,equipo,marca,iden,capac_pk,obs) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                    (llave_form, fecha_form, 'PR-INSP-006', revis, nivel_il, con_sup, met_insp, tipo_il, check1, check2, check3, detalle, 'PR-INSP-007', revis_p, temp_ens, tipo_il_p, nivel_il_p, mater_base, tipo_sec, marca_pk, iden_pk, modelo_pk, vt, pt,  'II VISIBLE', 'Met-L-Chek  VP-31A', '5 minutos', 'REMOVIBLE SOLVENTE', 'Met-L-Chek   E-59A', '10 minutos', 'SOLVENTE REMOVED', 'Met-L-Chek   D-70', '10 minutos', equipo, marca, capac_pk, iden, obs))
        mysql.connection.commit()
        return redirect(url_for('resum_frqru'))
    return render_template('frqru.html', form=form)




@app.route('/edit_frqru/<id>', methods=['POST', 'GET'])
@login_required
def get_frqru(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM frqru WHERE id = %s', (id,))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-frqru.html', contact=data[0])



@app.route('/update_frqru/<id>', methods=['POST'])
@login_required
def update_frqru(id):
    if request.method == 'POST':
        proc = request.form['proc']
        revis = request.form['revis']
        nivel_il = request.form['nivel_il']
        con_sup = request.form['con_sup']
        met_insp = request.form['met_insp']
        tipo_il = request.form['tipo_il']
        check1 = request.form['check1']
        check2 = request.form['check2']
        check3 = request.form['check3']
        detalle = request.form['detalle']
        proc_p = request.form['proc_p']
        revis_p = request.form['revis_p']
        temp_ens = request.form['temp_ens']
        tipo_il_p = request.form['tipo_il_p']
        nivel_il_p = request.form['nivel_il_p']
        mater_base = request.form['mater_base']
        tipo_sec = request.form['tipo_sec']
        tipo_pen = request.form['tipo_pen']
        marca_kit = request.form['marca_kit']
        tiem_pen = request.form['tiem_pen']
        met_rem = request.form['met_rem']
        marca_kit1 = request.form['marca_kit1']
        tiem_sec = request.form['tiem_sec']
        for_rev = request.form['for_rev']
        marca_kit2 = request.form['marca_kit2']
        tiem_rev = request.form['tiem_rev']
        equipo = request.form['equipo']
        marca = request.form['marca']
        iden = request.form['iden']
        marca_pk = request.form['marca_pk']
        iden_pk = request.form['iden_pk']
        modelo_pk = request.form['modelo_pk']
        capac_pk = request.form['capac_pk']
        obs = request.form['obs']
        vt = request.form['vt']
        pt = request.form['pt']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE frqru
            SET proc = %s,
                revis = %s,
                nivel_il = %s,
				con_sup = %s,
                met_insp = %s,
				tipo_il = %s,
                check1 = %s,
				check2 = %s,
                check3 = %s,
				detalle = %s,
                proc_p = %s,
				revis_p = %s,
                temp_ens = %s,
				tipo_il_p = %s,
                nivel_il_p = %s,
				mater_base = %s,
                tipo_sec = %s,
				tipo_pen = %s,
                marca_kit = %s,
				tiem_pen = %s,
                met_rem = %s,
				marca_kit1 = %s,
                tiem_sec = %s,
				for_rev = %s,
                marca_kit2 = %s,
				tiem_rev = %s,
                equipo = %s,
				marca = %s,
                iden = %s,
                marca_pk = %s,
                iden_pk = %s,
                modelo_pk = %s,
                capac_pk = %s,
                obs = %s,
                vt = %s,
                pt = %s
            WHERE id = %s
        """, (proc, revis, nivel_il, con_sup, met_insp, tipo_il, check1, check2, check3, detalle, proc_p, revis_p, temp_ens, tipo_il_p, nivel_il_p, mater_base, tipo_sec, tipo_pen, marca_kit, tiem_pen, met_rem, marca_kit1, tiem_sec, for_rev, marca_kit2, tiem_rev, equipo, marca, iden, marca_pk, iden_pk, modelo_pk, capac_pk,obs,vt,pt,id))
        flash('Contact Updated Successfully')
        mysql.connection.commit()
        return redirect(url_for('resum_frqru'))

@app.route('/resum_frqru')
@login_required
def resum_frqru():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select * from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    datos = cursor.fetchall()
    cursor.execute(
        "select num_rep from formulario where id_formulario = (select MAX(b.id_formulario) from formulario a inner join frqru b on a.id_formulario = b.id_formulario);")
    num_rep = cursor.fetchone()
    cursor.execute(
        "select * from frqru where id_formulario = (select MAX(b.id_formulario) from formulario a inner join frqru b on a.id_formulario = b.id_formulario);")
    datos1 = cursor.fetchall()
    cursor.execute(
        "select MAX(id) from frqru ;")
    data1 = cursor.fetchone()
    cursor.execute(
        "select descr from cat_form where codigo = 'FR-INSP-055.04';")
    cata = cursor.fetchone()
    print(data1)
    
    return render_template('resum_frqru.html', datos=datos,num_rep=num_rep,datos1=datos1, contact=data1[0],cata=cata)


@app.route('/genera_pdffrqru2')
@login_required
def genera_pdffrqru2():
    options = {
        'dpi': '300',
        'page-size': 'A4',
        # 'orientation': 'Landscape',
        'margin-top': '0mm',
        'margin-right': '20mm',
        'margin-bottom': '20mm',
        'margin-left': '10mm',
        'encoding': "UTF-8",
        #'grayscale': None,
        'outline-depth':3,
        # 'footer-center':'[page]',
        'footer-line': None,
        "enable-local-file-access": None,
    }
    path = r'C:/Ricardo/paginas_web/u30/aplicacion/static/css/'
    css = [path + 'style.css']

    path_wkhtmltopdf = r'C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe'
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select llave_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    nom_form = cursor.fetchone()
    cursor.execute(
        "select num_rep from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    num_rep = cursor.fetchone()
    cursor.execute(
        "select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_insp = cursor.fetchone()
    cursor.execute(
        "select fecha_emision_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_emi = cursor.fetchone()
    cursor.execute(
        "select fecha_expiracion_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_exp = cursor.fetchone()
    cursor.execute(
        "select lugar_ins_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    lugar = cursor.fetchone()
    cursor.execute(
        "select nom_inspe_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    inpe = cursor.fetchone()
    cursor.execute(
        "select * from frqru where id_formulario = (select MAX(id_formulario) from formulario);")
    datos1 = cursor.fetchall()
    cursor.execute(
        "select MAX(id) from frqru ;")
    data1 = cursor.fetchone()
    html = render_template('resum_frqru_1.html', datos=nom_form,num_rep=num_rep, fec1=fec_insp, fec2=fec_emi, fec3=fec_exp, lugar=lugar, inspector=inpe, datos1=datos1, contact=data1[0])
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    #pdfkit.from_file("aplicacion/templates/cert_for1.html", "index.pdf", options=options,configuration=config)
    pdfkit.from_string(html, "resum_frqru_1.pdf", options=options,configuration=config)
    #pdfkit.from_url("http://127.0.0.1:5000/cert_for1", "cert_for1.pdf",options=options,configuration=config)
    print("="*50)
    return redirect(url_for('cert_for8'))

@app.route('/reporte_fotofrqru')
@login_required
def reporte_fotofrqru():
    lista = []
    for file in listdir(app.root_path+"/static/img/subidas/frqru/"):
        lista.append(file)
    return render_template("reporte_fotofrqru.html", lista=lista)


@app.route('/upload_frqru', methods=['get', 'post'])
def upload_frqru():
    form = UploadForm()  # carga request.from y request.file
    if form.validate_on_submit():
        f = form.photo.data
        filename = secure_filename(f.filename)
        f.save(app.root_path+"/static/img/subidas/frqru/"+filename)
        foto = app.root_path+"/static/img/subidas/frqru/"+filename
        cursor = mysql.connection.cursor()
        cursor.execute(
            "select id from frqru where id = (select MAX(id) from frqru) ;")
        llave_form = cursor.fetchone()
        cursor.execute('insert into rep_foto_frqru (foto,id_f) VALUES (%s,%s)',
                    ( foto,llave_form))
        mysql.connection.commit()
        return redirect(url_for('inicio_fotofrqru'))
    return render_template('upload_frqru.html', form=form)

@app.route('/inicio_fotofrqru')
@login_required
def inicio_fotofrqru():
    lista = []
    for file in listdir(app.root_path+"/static/img/subidas/frqru/"):
        lista.append(file)
    return render_template("inicio_fotofrqru.html", lista=lista)


@app.route('/cert_for8', methods=['GET', 'POST'])
@login_required
def cert_for8():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select equipo from frqru where id_formulario = (select MAX(id_formulario) from formulario);")
    equipo = cursor.fetchone()
    cursor.execute(
        "select marca_pk from frqru where id_formulario = (select MAX(id_formulario) from formulario);")
    marca_pk = cursor.fetchone()
    cursor.execute(
        "select modelo_pk from frqru where id_formulario = (select MAX(id_formulario) from formulario);")
    modelo_pk = cursor.fetchone()
    cursor.execute(
        "select iden_pk from frqru where id_formulario = (select MAX(id_formulario) from formulario);")
    iden_pk = cursor.fetchone()
    cursor.execute(
        "select capac_pk from frqru where id_formulario = (select MAX(id_formulario) from formulario);")
    capac_pk = cursor.fetchone()
    cursor.execute(
        "select fecha_emision_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_emi = cursor.fetchone()
    cursor.execute(
        "select fecha_expiracion_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_exp = cursor.fetchone()
    cursor.execute(
        "select num_rep from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    llave = cursor.fetchone()
    cursor.execute(
        "select empresa from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    emp = cursor.fetchone()
    cursor.execute(
        "select lugar_ins_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    lug = cursor.fetchone()
    cursor.execute(
        "select nom_inspe_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    ins = cursor.fetchone()
    return render_template('cert_for8.html', equipo=equipo, marca_pk=marca_pk, modelo_pk=modelo_pk, iden_pk=iden_pk, capac_pk=capac_pk, fec_emi=fec_emi, fec_exp=fec_exp, llave=llave, emp=emp, lug=lug, ins=ins)

@app.route('/genera_pdffrqru')
@login_required
def genera_pdffrqru():
    options = {
        'page-size': 'A4',
        # 'orientation': 'Landscape',
        'margin-top': '20mm',
        'margin-right': '20mm',
        'margin-bottom': '20mm',
        'margin-left': '20mm',
        'encoding': "UTF-8",
        'outline-depth':3,
        # 'footer-center':'[page]',
        'footer-line': None,
        "enable-local-file-access": None,
    }
    path_wkhtmltopdf = r'C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe'
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select equipo from frqru where id_formulario = (select MAX(id_formulario) from formulario);")
    equipo = cursor.fetchone()
    cursor.execute(
        "select marca_pk from frqru where id_formulario = (select MAX(id_formulario) from formulario);")
    marca_pk = cursor.fetchone()
    cursor.execute(
        "select modelo_pk from frqru where id_formulario = (select MAX(id_formulario) from formulario);")
    modelo_pk = cursor.fetchone()
    cursor.execute(
        "select iden_pk from frqru where id_formulario = (select MAX(id_formulario) from formulario);")
    iden_pk = cursor.fetchone()
    cursor.execute(
        "select capac_pk from frqru where id_formulario = (select MAX(id_formulario) from formulario);")
    capac_pk = cursor.fetchone()
    cursor.execute(
        "select fecha_emision_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_emi = cursor.fetchone()
    cursor.execute(
        "select fecha_expiracion_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_exp = cursor.fetchone()
    cursor.execute(
        "select num_rep from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    llave = cursor.fetchone()
    cursor.execute(
        "select empresa from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    emp = cursor.fetchone()
    cursor.execute(
        "select lugar_ins_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    lug = cursor.fetchone()
    cursor.execute(
        "select nom_inspe_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    ins = cursor.fetchone()
    html = render_template('cert_for8.html', equipo=equipo, marca_pk=marca_pk, modelo_pk=modelo_pk, iden_pk=iden_pk, capac_pk=capac_pk, fec_emi=fec_emi, fec_exp=fec_exp, llave=llave, emp=emp, lug=lug, ins=ins)
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    #pdfkit.from_file("aplicacion/templates/cert_for1.html", "index.pdf", options=options,configuration=config)
    pdfkit.from_string(html, "cert_for8.pdf", options=options,configuration=config)
    print("="*50)
    return redirect(url_for('inicio'))


@app.route('/home_9', methods=['GET', 'POST'])
@login_required
def home_9():
    cursor = mysql.connection.cursor()
    cursor.execute("select nombre from articulos where id =13;")
    nom_form = cursor.fetchone()
    cursor.execute("select descripcion from articulos where id = 13;")
    nom_form1 = cursor.fetchone()
    form = datos_reporte()
    if form.validate_on_submit():
        cur = mysql.connection.cursor()
        cur.execute("select (sec+1) from cod_rep where id = 21;")
        sec = cur.fetchone()
        print(sec)
        cur.execute("""
                    UPDATE cod_rep
                    SET sec = %s
                        WHERE id = 21
                """, sec)
        mysql.connection.commit()
        empre = request.form['empresa']
        cur.execute(
            "select CONCAT(prefijo,LPAD(sec, 5, '0')) from cod_rep where id_for = 10;")
        num_rep = cur.fetchone()
        fecha_insp = request.form['fec_inpec']
        fecha_emi = request.form['fec_emision']
        fecha_exp = request.form['fec_expiracion']
        lugar_ins = request.form['lugar_inpec']
        nombre_ins = request.form['nom_inspec']
        cursor = mysql.connection.cursor()
        cursor.execute('insert into formulario (llave_formulario,num_rep,desc_formulario,fecha_inspec_formulario,fecha_emision_formulario,fecha_expiracion_formulario,lugar_ins_formulario,nom_inspe_formulario,empresa,cod_form) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                       (nom_form,num_rep, nom_form1, fecha_insp, fecha_emi, fecha_exp, lugar_ins, nombre_ins, empre,'frsep'))
        mysql.connection.commit()
        flash('Guardado Correctamente')
        datos = cursor.fetchone()
        print(datos)
        # return 'OK'
        return redirect(url_for('frsep'))
    return render_template('home_9.html', form=form, datos=nom_form, desc=nom_form1)


@app.route('/frsep', methods=['GET', 'POST'])
@login_required
def frsep():
    form = formu9()
    if form.validate_on_submit():
        revis = request.form['revis']
        nivel_il = request.form['nivel_il']
        con_sup = request.form['con_sup']
        met_insp = request.form['met_insp']
        tipo_il = request.form['tipo_il']
        check1 = request.form['check1']
        check2 = request.form['check2']
        check3 = request.form['check3']
        detalle = request.form['detalle']
        revis_p = request.form['revis_p']
        temp_ens = request.form['temp_ens']
        tipo_il_p = request.form['tipo_il_p']
        nivel_il_p = request.form['nivel_il_p']
        mater_base = request.form['mater_base']
        tipo_sec = request.form['tipo_sec']
        marca_pk = request.form['marca_pk']
        iden_pk = request.form['iden_pk']
        modelo_pk = request.form['modelo_pk']
        capac_pk = request.form['capac_pk']
        obs = request.form['obs']
        vt = request.form['vt']
        pt = request.form['pt']
        cur = mysql.connection.cursor()
        cur.execute(
            "select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
        llave_form = cur.fetchone()
        cur.execute(
            "select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
        fecha_form = cur.fetchone()
        cur.execute('insert into frsep (id_formulario,fec_formulario,proc,revis,nivel_il,con_sup,met_insp,tipo_il,check1,check2,check3,detalle,proc_p,revis_p,temp_ens,tipo_il_p,nivel_il_p,mater_base,tipo_sec,marca_pk,iden_pk,modelo_pk,vt,pt,tipo_pen,marca_kit,tiem_pen,met_rem,marca_kit1,tiem_sec,for_rev,marca_kit2,tiem_rev,capac_pk,obs) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                    (llave_form, fecha_form, 'PR-INSP-006', revis, nivel_il, con_sup, met_insp, tipo_il, check1, check2, check3, detalle, 'PR-INSP-007', revis_p, temp_ens, tipo_il_p, nivel_il_p, mater_base, tipo_sec, marca_pk, iden_pk, modelo_pk, vt, pt,'II VISIBLE', 'Met-L-Chek  VP-31A', '5 minutos', 'REMOVIBLE SOLVENTE', 'Met-L-Chek   E-59A', '10 minutos', 'SOLVENTE REMOVED', 'Met-L-Chek   D-70', '10 minutos' , capac_pk, obs))
        mysql.connection.commit()
        return redirect(url_for('resum_frsep'))
    return render_template('frsep.html', form=form)



@app.route('/edit_frsep/<id>', methods=['POST', 'GET'])
@login_required
def get_frsep(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM frsep WHERE id = %s', (id,))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-frsep.html', contact=data[0])



@app.route('/update_frsep/<id>', methods=['POST'])
@login_required
def update_frsep(id):
    if request.method == 'POST':
        proc = request.form['proc']
        revis = request.form['revis']
        nivel_il = request.form['nivel_il']
        con_sup = request.form['con_sup']
        met_insp = request.form['met_insp']
        tipo_il = request.form['tipo_il']
        check1 = request.form['check1']
        check2 = request.form['check2']
        check3 = request.form['check3']
        detalle = request.form['detalle']
        proc_p = request.form['proc_p']
        revis_p = request.form['revis_p']
        temp_ens = request.form['temp_ens']
        tipo_il_p = request.form['tipo_il_p']
        nivel_il_p = request.form['nivel_il_p']
        mater_base = request.form['mater_base']
        tipo_sec = request.form['tipo_sec']
        tipo_pen = request.form['tipo_pen']
        marca_kit = request.form['marca_kit']
        tiem_pen = request.form['tiem_pen']
        met_rem = request.form['met_rem']
        marca_kit1 = request.form['marca_kit1']
        tiem_sec = request.form['tiem_sec']
        for_rev = request.form['for_rev']
        marca_kit2 = request.form['marca_kit2']
        tiem_rev = request.form['tiem_rev']
        obs = request.form['obs']
        vt = request.form['vt']
        pt = request.form['pt']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE frsep
            SET proc = %s,
                revis = %s,
                nivel_il = %s,
				con_sup = %s,
                met_insp = %s,
				tipo_il = %s,
                check1 = %s,
				check2 = %s,
                check3 = %s,
				detalle = %s,
                proc_p = %s,
				revis_p = %s,
                temp_ens = %s,
				tipo_il_p = %s,
                nivel_il_p = %s,
				mater_base = %s,
                tipo_sec = %s,
				tipo_pen = %s,
                marca_kit = %s,
				tiem_pen = %s,
                met_rem = %s,
				marca_kit1 = %s,
                tiem_sec = %s,
				for_rev = %s,
                marca_kit2 = %s,
				tiem_rev = %s,
                obs = %s,
                vt = %s,
                pt = %s
            WHERE id = %s
        """, (proc, revis, nivel_il, con_sup, met_insp, tipo_il, check1, check2, check3, detalle, proc_p, revis_p, temp_ens, tipo_il_p, nivel_il_p, mater_base, tipo_sec, tipo_pen, marca_kit, tiem_pen, met_rem, marca_kit1, tiem_sec, for_rev, marca_kit2, tiem_rev,obs,vt,pt,id))
        flash('Contact Updated Successfully')
        mysql.connection.commit()
        return redirect(url_for('resum_frsep'))

@app.route('/resum_frsep')
@login_required
def resum_frsep():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select * from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    datos = cursor.fetchall()
    cursor.execute(
        "select num_rep from formulario where id_formulario = (select MAX(b.id_formulario) from formulario a inner join frsep b on a.id_formulario = b.id_formulario);")
    num_rep = cursor.fetchone()
    cursor.execute(
        "select * from frsep where id_formulario = (select MAX(b.id_formulario) from formulario a inner join frsep b on a.id_formulario = b.id_formulario);")
    datos1 = cursor.fetchall()
    cursor.execute(
        "select MAX(id) from frsep ;")
    data1 = cursor.fetchone()
    cursor.execute(
        "select descr from cat_form where codigo = 'FR-INSP-057.04';")
    cata = cursor.fetchone()
    print(data1)
    
    return render_template('resum_frsep.html', datos=datos,num_rep=num_rep,datos1=datos1, contact=data1[0],cata=cata)


@app.route('/genera_pdffrsep2')
@login_required
def genera_pdffrsep2():
    options = {
        'dpi': '300',
        'page-size': 'A4',
        # 'orientation': 'Landscape',
        'margin-top': '0mm',
        'margin-right': '20mm',
        'margin-bottom': '20mm',
        'margin-left': '10mm',
        'encoding': "UTF-8",
        #'grayscale': None,
        'outline-depth':3,
        # 'footer-center':'[page]',
        'footer-line': None,
        "enable-local-file-access": None,
    }
    path = r'C:/Ricardo/paginas_web/u30/aplicacion/static/css/'
    css = [path + 'style.css']

    path_wkhtmltopdf = r'C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe'
    cursor = mysql.connection.cursor()
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select llave_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    nom_form = cursor.fetchone()
    cursor.execute(
        "select num_rep from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    num_rep = cursor.fetchone()
    cursor.execute(
        "select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_insp = cursor.fetchone()
    cursor.execute(
        "select fecha_emision_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_emi = cursor.fetchone()
    cursor.execute(
        "select fecha_expiracion_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_exp = cursor.fetchone()
    cursor.execute(
        "select lugar_ins_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    lugar = cursor.fetchone()
    cursor.execute(
        "select nom_inspe_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    inpe = cursor.fetchone()
    cursor.execute(
        "select * from frsep where id_formulario = (select MAX(id_formulario) from formulario);")
    datos1 = cursor.fetchall()
    cursor.execute(
        "select MAX(id) from frsep ;")
    data1 = cursor.fetchone()
    html = render_template('resum_frsep_1.html', datos=nom_form,num_rep=num_rep, fec1=fec_insp, fec2=fec_emi, fec3=fec_exp, lugar=lugar, inspector=inpe, datos1=datos1, contact=data1[0])
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    #pdfkit.from_file("aplicacion/templates/cert_for1.html", "index.pdf", options=options,configuration=config)
    pdfkit.from_string(html, "resum_frsep_1.pdf", options=options,configuration=config)
    #pdfkit.from_url("http://127.0.0.1:5000/cert_for1", "cert_for1.pdf",options=options,configuration=config)
    print("="*50)
    return redirect(url_for('cert_for9'))

@app.route('/reporte_fotofrsep')
@login_required
def reporte_fotofrsep():
    lista = []
    for file in listdir(app.root_path+"/static/img/subidas/frsep/"):
        lista.append(file)
    return render_template("reporte_fotofrsep.html", lista=lista)


@app.route('/upload_frsep', methods=['get', 'post'])
def upload_frsep():
    form = UploadForm()  # carga request.from y request.file
    if form.validate_on_submit():
        f = form.photo.data
        filename = secure_filename(f.filename)
        f.save(app.root_path+"/static/img/subidas/frsep/"+filename)
        foto = app.root_path+"/static/img/subidas/frsep/"+filename
        cursor = mysql.connection.cursor()
        cursor.execute(
            "select id from frsep where id = (select MAX(id) from frsep) ;")
        llave_form = cursor.fetchone()
        cursor.execute('insert into rep_foto_frsep (foto,id_f) VALUES (%s,%s)',
                    ( foto,llave_form))
        mysql.connection.commit()
        return redirect(url_for('inicio_fotofrsep'))
    return render_template('upload_frsep.html', form=form)

@app.route('/inicio_fotofrsep')
@login_required
def inicio_fotofrsep():
    lista = []
    for file in listdir(app.root_path+"/static/img/subidas/frsep/"):
        lista.append(file)
    return render_template("inicio_fotofrsep.html", lista=lista)
    
    


@app.route('/cert_for9', methods=['GET', 'POST'])
@login_required
def cert_for9():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select marca_pk from frsep where id_formulario = (select MAX(id_formulario) from formulario);")
    marca_pk = cursor.fetchone()
    cursor.execute(
        "select modelo_pk from frsep where id_formulario = (select MAX(id_formulario) from formulario);")
    modelo_pk = cursor.fetchone()
    cursor.execute(
        "select iden_pk from frsep where id_formulario = (select MAX(id_formulario) from formulario);")
    iden_pk = cursor.fetchone()
    cursor.execute(
        "select capac_pk from frsep where id_formulario = (select MAX(id_formulario) from formulario);")
    capac_pk = cursor.fetchone()
    cursor.execute(
        "select fecha_emision_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_emi = cursor.fetchone()
    cursor.execute(
        "select fecha_expiracion_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_exp = cursor.fetchone()
    cursor.execute(
        "select num_rep from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    llave = cursor.fetchone()
    cursor.execute(
        "select empresa from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    emp = cursor.fetchone()
    cursor.execute(
        "select lugar_ins_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    lug = cursor.fetchone()
    cursor.execute(
        "select nom_inspe_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    ins = cursor.fetchone()
    return render_template('cert_for9.html', marca_pk=marca_pk, modelo_pk=modelo_pk, iden_pk=iden_pk, capac_pk=capac_pk, fec_emi=fec_emi, fec_exp=fec_exp, llave=llave, emp=emp, lug=lug, ins=ins)


@app.route('/genera_pdffrsep')
@login_required
def genera_pdffrsep():
    options = {
        'page-size': 'A4',
        # 'orientation': 'Landscape',
        'margin-top': '20mm',
        'margin-right': '20mm',
        'margin-bottom': '20mm',
        'margin-left': '20mm',
        'encoding': "UTF-8",
        'outline-depth':3,
        # 'footer-center':'[page]',
        'footer-line': None,
        "enable-local-file-access": None,
    }
    path_wkhtmltopdf = r'C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe'
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select marca_pk from frsep where id_formulario = (select MAX(id_formulario) from formulario);")
    marca_pk = cursor.fetchone()
    cursor.execute(
        "select modelo_pk from frsep where id_formulario = (select MAX(id_formulario) from formulario);")
    modelo_pk = cursor.fetchone()
    cursor.execute(
        "select iden_pk from frsep where id_formulario = (select MAX(id_formulario) from formulario);")
    iden_pk = cursor.fetchone()
    cursor.execute(
        "select capac_pk from frsep where id_formulario = (select MAX(id_formulario) from formulario);")
    capac_pk = cursor.fetchone()
    cursor.execute(
        "select fecha_emision_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_emi = cursor.fetchone()
    cursor.execute(
        "select fecha_expiracion_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_exp = cursor.fetchone()
    cursor.execute(
        "select num_rep from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    llave = cursor.fetchone()
    cursor.execute(
        "select empresa from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    emp = cursor.fetchone()
    cursor.execute(
        "select lugar_ins_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    lug = cursor.fetchone()
    cursor.execute(
        "select nom_inspe_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    ins = cursor.fetchone()
    html = render_template('cert_for9.html', marca_pk=marca_pk, modelo_pk=modelo_pk, iden_pk=iden_pk, capac_pk=capac_pk, fec_emi=fec_emi, fec_exp=fec_exp, llave=llave, emp=emp, lug=lug, ins=ins)
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    #pdfkit.from_file("aplicacion/templates/cert_for1.html", "index.pdf", options=options,configuration=config)
    pdfkit.from_string(html, "cert_for9.pdf", options=options,configuration=config)
    print("="*50)
    return redirect(url_for('inicio'))


@app.route('/home_10', methods=['GET', 'POST'])
@login_required
def home_10():
    cursor = mysql.connection.cursor()
    cursor.execute("select nombre from articulos where id =14;")
    nom_form = cursor.fetchone()
    cursor.execute("select descripcion from articulos where id = 14;")
    nom_form1 = cursor.fetchone()
    form = datos_reporte()
    if form.validate_on_submit():
        cur = mysql.connection.cursor()
        cur.execute("select (sec+1) from cod_rep where id = 22;")
        sec = cur.fetchone()
        print(sec)
        cur.execute("""
                    UPDATE cod_rep
                    SET sec = %s
                        WHERE id = 22
                """, sec)
        mysql.connection.commit()
        empre = request.form['empresa']
        cur.execute(
            "select CONCAT(prefijo,LPAD(sec, 5, '0')) from cod_rep where id_for = 11;")
        num_rep = cur.fetchone()
        fecha_insp = request.form['fec_inpec']
        fecha_emi = request.form['fec_emision']
        fecha_exp = request.form['fec_expiracion']
        lugar_ins = request.form['lugar_inpec']
        nombre_ins = request.form['nom_inspec']
        cursor = mysql.connection.cursor()
        cursor.execute('insert into formulario (llave_formulario,num_rep,desc_formulario,fecha_inspec_formulario,fecha_emision_formulario,fecha_expiracion_formulario,lugar_ins_formulario,nom_inspe_formulario,empresa,cod_form) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                       (nom_form,num_rep, nom_form1, fecha_insp, fecha_emi, fecha_exp, lugar_ins, nombre_ins, empre,'frhor'))
        mysql.connection.commit()
        flash('Guardado Correctamente')
        datos = cursor.fetchone()
        print(datos)
        # return 'OK'
        return redirect(url_for('frhor'))
    return render_template('home_10.html', form=form, datos=nom_form, desc=nom_form1)


@app.route('/frhor', methods=['GET', 'POST'])
@login_required
def frhor():
    form = formu10()
    if form.validate_on_submit():
        revis = request.form['revis']
        nivel_il = request.form['nivel_il']
        con_sup = request.form['con_sup']
        met_insp = request.form['met_insp']
        tipo_il = request.form['tipo_il']
        check1 = request.form['check1']
        check2 = request.form['check2']
        check3 = request.form['check3']
        detalle = request.form['detalle']
        revis_p = request.form['revis_p']
        temp_ens = request.form['temp_ens']
        tipo_il_p = request.form['tipo_il_p']
        nivel_il_p = request.form['nivel_il_p']
        mater_base = request.form['mater_base']
        tipo_sec = request.form['tipo_sec']
        equipo = request.form['equipo']
        modelo = request.form['modelo']
        iden = request.form['iden']
        marca_hd = request.form['marca_hd']
        iden_hd = request.form['iden_hd']
        modelo_hd = request.form['modelo_hd']
        capac_hd = request.form['capac_hd']
        medidas_hd = request.form['medidas_hd']
        marca_hi = request.form['marca_hi']
        iden_hi = request.form['iden_hi']
        modelo_hi = request.form['modelo_hi']
        capac_hi = request.form['capac_hi']
        medidas_hi = request.form['medidas_hi']
        desghd = request.form['desghd']
        desapd = request.form['desapd']
        vastagod = request.form['vastagod']
        hojad = request.form['hojad']
        angulod = request.form['angulod']
        obsd = request.form['obsd']
        vtd = request.form['vtd']
        ptd = request.form['ptd']
        desghi = request.form['desghi']
        desapi = request.form['desapi']
        vastagoi = request.form['vastagoi']
        hojai = request.form['hojai']
        anguloi = request.form['anguloi']
        obsi = request.form['obsi']
        vti = request.form['vti']
        pti = request.form['pti']
        cur = mysql.connection.cursor()
        cur.execute(
            "select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
        llave_form = cur.fetchone()
        cur.execute(
            "select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
        fecha_form = cur.fetchone()
        cur.execute('insert into frhor (id_formulario,fec_formulario,proc,revis,nivel_il,con_sup,met_insp,tipo_il,check1,check2,check3,detalle,proc_p,revis_p,temp_ens,tipo_il_p,nivel_il_p,mater_base,tipo_sec,tipo_pen,marca_kit,tiem_pen,met_rem,marca_kit1,tiem_sec,for_rev,marca_kit2,tiem_rev,equipo,modelo,iden,marca_hd,iden_hd,modelo_hd,capac_hd,medidas_hd,marca_hi,iden_hi,modelo_hi,capac_hi,medidas_hi, desghd,desapd,vastagod,hojad,angulod,obsd,vtd,ptd,desghi,desapi,vastagoi,hojai,anguloi,obsi,vti,pti) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                    (llave_form, fecha_form, 'PR-INSP-006', revis, nivel_il, con_sup, met_insp, tipo_il, check1, check2, check3, detalle, 'PR-INSP-007', revis_p, temp_ens, tipo_il_p, nivel_il_p, mater_base, tipo_sec,'II VISIBLE', 'Met-L-Chek  VP-31A', '5 minutos', 'REMOVIBLE SOLVENTE', 'Met-L-Chek   E-59A', '10 minutos', 'SOLVENTE REMOVED', 'Met-L-Chek   D-70', '10 minutos' , equipo, modelo, iden, marca_hd, iden_hd, modelo_hd, capac_hd, medidas_hd, marca_hi, iden_hi, modelo_hi, capac_hi, medidas_hi,desghd,desapd,vastagod,hojad,angulod,obsd,vtd,ptd,desghi,desapi,vastagoi,hojai,anguloi,obsi,vti,pti))
        mysql.connection.commit()
        return redirect(url_for('resum_frhor'))

    return render_template('frhor.html', form=form)



@app.route('/edit_frhor/<id>', methods=['POST', 'GET'])
@login_required
def get_frhor(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM frhor WHERE id = %s', (id,))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-frhor.html', contact=data[0])



@app.route('/update_frhor/<id>', methods=['POST'])
@login_required
def update_frhor(id):
    if request.method == 'POST':
        proc = request.form['proc']
        revis = request.form['revis']
        nivel_il = request.form['nivel_il']
        con_sup = request.form['con_sup']
        met_insp = request.form['met_insp']
        tipo_il = request.form['tipo_il']
        check1 = request.form['check1']
        check2 = request.form['check2']
        check3 = request.form['check3']
        detalle = request.form['detalle']
        proc_p = request.form['proc_p']
        revis_p = request.form['revis_p']
        temp_ens = request.form['temp_ens']
        tipo_il_p = request.form['tipo_il_p']
        nivel_il_p = request.form['nivel_il_p']
        mater_base = request.form['mater_base']
        tipo_sec = request.form['tipo_sec']
        tipo_pen = request.form['tipo_pen']
        marca_kit = request.form['marca_kit']
        tiem_pen = request.form['tiem_pen']
        met_rem = request.form['met_rem']
        marca_kit1 = request.form['marca_kit1']
        tiem_sec = request.form['tiem_sec']
        for_rev = request.form['for_rev']
        marca_kit2 = request.form['marca_kit2']
        tiem_rev = request.form['tiem_rev']
        equipo = request.form['equipo']
        marca = request.form['marca']
        iden = request.form['iden']
        marca_hd = request.form['marca_hd']
        iden_hd = request.form['iden_hd']
        modelo_hd = request.form['modelo_hd']
        capac_hd = request.form['capac_hd']
        medidas_hd = request.form['medidas_hd']
        marca_hi = request.form['marca_hi']
        iden_hi = request.form['iden_hi']
        modelo_hi = request.form['modelo_hi']
        capac_hi = request.form['capac_hi']
        obs = request.form['obs']
        vt = request.form['vt']
        pt = request.form['pt']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE frhor
            SET proc = %s,
                revis = %s,
                nivel_il = %s,
				con_sup = %s,
                met_insp = %s,
				tipo_il = %s,
                check1 = %s,
				check2 = %s,
                check3 = %s,
				detalle = %s,
                proc_p = %s,
				revis_p = %s,
                temp_ens = %s,
				tipo_il_p = %s,
                nivel_il_p = %s,
				mater_base = %s,
                tipo_sec = %s,
				tipo_pen = %s,
                marca_kit = %s,
				tiem_pen = %s,
                met_rem = %s,
				marca_kit1 = %s,
                tiem_sec = %s,
				for_rev = %s,
                marca_kit2 = %s,
				tiem_rev = %s,
                equipo = %s,
				marca = %s,
                iden = %s,
                marca_hd = %s,
                iden_hd = %s,
                modelo_hd = %s,
                capac_hd = %s,
                medidas_hd = %s,
                marca_hi = %s,
                iden_hi = %s,
                modelo_hi = %s,
                capac_hi = %s,
                medidas_hi = %s,
                med_asi_hd = %s,
                med_asi_hi = %s,
                obs = %s,
                vt = %s,
                pt = %s
            WHERE id = %s
        """, (proc, revis, nivel_il, con_sup, met_insp, tipo_il, check1, check2, check3, detalle, proc_p, revis_p, temp_ens, tipo_il_p, nivel_il_p, mater_base, tipo_sec, tipo_pen, marca_kit, tiem_pen, met_rem, marca_kit1, tiem_sec, for_rev, marca_kit2, tiem_rev, equipo, marca, iden,marca_hd, iden_hd, modelo_hd, capac_hd, medidas_hd, marca_hi, iden_hi, modelo_hi, capac_hi, obs,vt,pt,id))
        flash('Contact Updated Successfully')
        mysql.connection.commit()
        return redirect(url_for('resum_frhor'))

@app.route('/resum_frhor')
@login_required
def resum_frhor():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select * from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    datos = cursor.fetchall()
    cursor.execute(
        "select num_rep from formulario where id_formulario = (select MAX(b.id_formulario) from formulario a inner join frhor b on a.id_formulario = b.id_formulario);")
    num_rep = cursor.fetchone()
    cursor.execute(
        "select * from frhor where id_formulario = (select MAX(b.id_formulario) from formulario a inner join frhor b on a.id_formulario = b.id_formulario);")
    datos1 = cursor.fetchall()
    cursor.execute(
        "select MAX(id) from frhor ;")
    data1 = cursor.fetchone()
    cursor.execute(
        "select descr from cat_form where codigo = 'FR-INSP-059.04';")
    cata = cursor.fetchone()
    print(data1)
    return render_template('resum_frhor.html', datos=datos,num_rep=num_rep,datos1=datos1, contact=data1[0],cata=cata)

@app.route('/genera_pdffrhor2')
@login_required
def genera_pdffrhor2():
    options = {
        'dpi': '300',
        'page-size': 'A4',
        # 'orientation': 'Landscape',
        'margin-top': '0mm',
        'margin-right': '20mm',
        'margin-bottom': '20mm',
        'margin-left': '10mm',
        'encoding': "UTF-8",
        #'grayscale': None,
        'outline-depth':3,
        # 'footer-center':'[page]',
        'footer-line': None,
        "enable-local-file-access": None,
    }
    path = r'C:/Ricardo/paginas_web/u30/aplicacion/static/css/'
    css = [path + 'style.css']

    path_wkhtmltopdf = r'C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe'
    cursor = mysql.connection.cursor()
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select llave_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    nom_form = cursor.fetchone()
    cursor.execute(
        "select num_rep from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    num_rep = cursor.fetchone()
    cursor.execute(
        "select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_insp = cursor.fetchone()
    cursor.execute(
        "select fecha_emision_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_emi = cursor.fetchone()
    cursor.execute(
        "select fecha_expiracion_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_exp = cursor.fetchone()
    cursor.execute(
        "select lugar_ins_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    lugar = cursor.fetchone()
    cursor.execute(
        "select nom_inspe_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    inpe = cursor.fetchone()
    cursor.execute(
        "select * from frhor where id_formulario = (select MAX(id_formulario) from formulario);")
    datos1 = cursor.fetchall()
    cursor.execute(
        "select MAX(id) from frhor ;")
    data1 = cursor.fetchone()
    html = render_template('resum_frhor_1.html', datos=nom_form, fec1=fec_insp, num_rep=num_rep,fec2=fec_emi, fec3=fec_exp, lugar=lugar, inspector=inpe, datos1=datos1, contact=data1[0])
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    #pdfkit.from_file("aplicacion/templates/cert_for1.html", "index.pdf", options=options,configuration=config)
    pdfkit.from_string(html, "resum_frhor_1.pdf", options=options,configuration=config)
    #pdfkit.from_url("http://127.0.0.1:5000/cert_for1", "cert_for1.pdf",options=options,configuration=config)
    print("="*50)
    return redirect(url_for('cert_for10'))

@app.route('/reporte_fotofrhor')
@login_required
def reporte_fotofrhor():
    lista = []
    for file in listdir(app.root_path+"/static/img/subidas/frhor/"):
        lista.append(file)
    return render_template("reporte_fotofrhor.html", lista=lista)


@app.route('/upload_frhor', methods=['get', 'post'])
def upload_frhor():
    form = UploadForm()  # carga request.from y request.file
    if form.validate_on_submit():
        f = form.photo.data
        filename = secure_filename(f.filename)
        f.save(app.root_path+"/static/img/subidas/frhor/"+filename)
        foto = app.root_path+"/static/img/subidas/frhor/"+filename
        cursor = mysql.connection.cursor()
        cursor.execute(
            "select id from frhor where id = (select MAX(id) from frhor) ;")
        llave_form = cursor.fetchone()
        cursor.execute('insert into rep_foto_frhor (foto,id_f) VALUES (%s,%s)',
                    ( foto,llave_form))
        mysql.connection.commit()
        return redirect(url_for('inicio_fotofrhor'))
    return render_template('upload_frhor.html', form=form)

@app.route('/inicio_fotofrhor')
@login_required
def inicio_fotofrhor():
    lista = []
    for file in listdir(app.root_path+"/static/img/subidas/frhor/"):
        lista.append(file)
    return render_template("inicio_fotofrhor.html", lista=lista)


@app.route('/cert_for10', methods=['GET', 'POST'])
@login_required
def cert_for10():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select * from frhor where id_formulario = (select MAX(id_formulario) from formulario);")
    datafr = cursor.fetchall()
    cursor.execute(
        "select * from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    data = cursor.fetchall()
    cursor.execute(
        "select fecha_expiracion_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_exp = cursor.fetchone()
    return render_template('cert_for10.html', datafr=datafr, data=data)



@app.route('/genera_pdffrhor')
@login_required
def genera_pdffrhor():
    options = {
        'page-size': 'A4',
        # 'orientation': 'Landscape',
        'margin-top': '20mm',
        'margin-right': '20mm',
        'margin-bottom': '20mm',
        'margin-left': '20mm',
        'encoding': "UTF-8",
        'outline-depth':3,
        # 'footer-center':'[page]',
        'footer-line': None,
        "enable-local-file-access": None,
    }
    path_wkhtmltopdf = r'C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe'
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select * from frhor where id_formulario = (select MAX(id_formulario) from formulario);")
    datafr = cursor.fetchall()
    cursor.execute(
        "select * from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    data = cursor.fetchall()
    cursor.execute(
        "select fecha_expiracion_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_exp = cursor.fetchone()
    html = render_template('cert_for10.html', datafr=datafr, data=data)
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    #pdfkit.from_file("aplicacion/templates/cert_for1.html", "index.pdf", options=options,configuration=config)
    pdfkit.from_string(html, "cert_for10.pdf", options=options,configuration=config)
    print("="*50)
    return redirect(url_for('inicio'))


@app.route('/home_11', methods=['GET', 'POST'])
@login_required
def home_11():
    cursor = mysql.connection.cursor()
    cursor.execute("select nombre from articulos where id =15;")
    nom_form = cursor.fetchone()
    cursor.execute("select descripcion from articulos where id = 15;")
    nom_form1 = cursor.fetchone()
    form = datos_reporte()
    if form.validate_on_submit():
        cur = mysql.connection.cursor()
        cur.execute("select (sec+1) from cod_rep where id = 23;")
        sec = cur.fetchone()
        print(sec)
        cur.execute("""
                    UPDATE cod_rep
                    SET sec = %s
                        WHERE id = 23
                """, sec)
        mysql.connection.commit()
        empre = request.form['empresa']
        cur.execute(
            "select CONCAT(prefijo,LPAD(sec, 5, '0')) from cod_rep where id_for = 12;")
        num_rep = cur.fetchone()
        fecha_insp = request.form['fec_inpec']
        fecha_emi = request.form['fec_emision']
        fecha_exp = request.form['fec_expiracion']
        lugar_ins = request.form['lugar_inpec']
        nombre_ins = request.form['nom_inspec']
        cursor = mysql.connection.cursor()
        cursor.execute('insert into formulario (llave_formulario,num_rep,desc_formulario,fecha_inspec_formulario,fecha_emision_formulario,fecha_expiracion_formulario,lugar_ins_formulario,nom_inspe_formulario,empresa,cod_form) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                       (nom_form,num_rep, nom_form1, fecha_insp, fecha_emi, fecha_exp, lugar_ins, nombre_ins, empre,'frppr'))
        mysql.connection.commit()
        flash('Guardado Correctamente')
        datos = cursor.fetchone()
        print(datos)
        # return 'OK'
        return redirect(url_for('frppr'))
    return render_template('home_11.html', form=form, datos=nom_form, desc=nom_form1)


@app.route('/frppr', methods=['GET', 'POST'])
@login_required
def frppr():
    form = formu11()
    if form.validate_on_submit():
        revis = request.form['revis']
        nivel_il = request.form['nivel_il']
        con_sup = request.form['con_sup']
        met_insp = request.form['met_insp']
        tipo_il = request.form['tipo_il']
        check1 = request.form['check1']
        check2 = request.form['check2']
        check3 = request.form['check3']
        detalle = request.form['detalle']
        revis_p = request.form['revis_p']
        temp_ens = request.form['temp_ens']
        tipo_il_p = request.form['tipo_il_p']
        nivel_il_p = request.form['nivel_il_p']
        mater_base = request.form['mater_base']
        tipo_sec = request.form['tipo_sec']
        equipo = request.form['equipo']
        modelo = request.form['modelo']
        iden = request.form['iden']
        marca_pas = request.form['marca_pas']
        iden_pas = request.form['iden_pas']
        modelo_pas = request.form['modelo_pas']
        capac_pas = request.form['capac_pas']
        numero = request.form['numero']
        asi_gan = request.form['asi_gan']
        gar_gan = request.form['gar_gan']
        med_gri = request.form['med_gri']
        obs = request.form['obs']
        vt = request.form['vt']
        pt = request.form['pt']
        cur = mysql.connection.cursor()
        cur.execute(
            "select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
        llave_form = cur.fetchone()
        cur.execute(
            "select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
        fecha_form = cur.fetchone()
        cur.execute('insert into frppr (id_formulario,fec_formulario,proc,revis,nivel_il,con_sup,met_insp,tipo_il,check1,check2,check3,detalle,proc_p,revis_p,temp_ens,tipo_il_p,nivel_il_p,mater_base,tipo_sec,tipo_pen,marca_kit,tiem_pen,met_rem,marca_kit1,tiem_sec,for_rev,marca_kit2,tiem_rev,equipo,modelo,iden,marca_pas,iden_pas,modelo_pas,capac_pas,numero,asi_gan,gar_gan,med_gri,obs,vt,pt,tipo_pa) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                    (llave_form, fecha_form, 'PR-INSP-006', revis, nivel_il, con_sup, met_insp, tipo_il, check1, check2, check3, detalle, 'PR-INSP-007', revis_p, temp_ens, tipo_il_p, nivel_il_p, mater_base, tipo_sec,'II VISIBLE', 'Met-L-Chek  VP-31A', '5 minutos', 'REMOVIBLE SOLVENTE', 'Met-L-Chek   E-59A', '10 minutos', 'SOLVENTE REMOVED', 'Met-L-Chek   D-70', '10 minutos' , equipo, modelo, iden, marca_pas, iden_pas, modelo_pas, capac_pas, numero, asi_gan, gar_gan, med_gri, obs, vt, pt,'1' ))
        mysql.connection.commit()
        return redirect(url_for('resum_frppr'))

    return render_template('frppr.html', form=form)



@app.route('/edit_frppr/<id>', methods=['POST', 'GET'])
@login_required
def get_frppr(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM frppr WHERE id = %s', (id,))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-frppr.html', contact=data[0])



@app.route('/update_frppr/<id>', methods=['POST'])
@login_required
def update_frppr(id):
    if request.method == 'POST':
        proc = request.form['proc']
        revis = request.form['revis']
        nivel_il = request.form['nivel_il']
        con_sup = request.form['con_sup']
        met_insp = request.form['met_insp']
        tipo_il = request.form['tipo_il']
        check1 = request.form['check1']
        check2 = request.form['check2']
        check3 = request.form['check3']
        detalle = request.form['detalle']
        proc_p = request.form['proc_p']
        revis_p = request.form['revis_p']
        temp_ens = request.form['temp_ens']
        tipo_il_p = request.form['tipo_il_p']
        nivel_il_p = request.form['nivel_il_p']
        mater_base = request.form['mater_base']
        tipo_sec = request.form['tipo_sec']
        tipo_pen = request.form['tipo_pen']
        marca_kit = request.form['marca_kit']
        tiem_pen = request.form['tiem_pen']
        met_rem = request.form['met_rem']
        marca_kit1 = request.form['marca_kit1']
        tiem_sec = request.form['tiem_sec']
        for_rev = request.form['for_rev']
        marca_kit2 = request.form['marca_kit2']
        tiem_rev = request.form['tiem_rev']
        equipo = request.form['equipo']
        marca = request.form['marca']
        iden = request.form['iden']
        marca_pas = request.form['marca_pas']
        iden_pas = request.form['iden_pas']
        modelo_pas = request.form['modelo_pas']
        capac_pas = request.form['capac_pas']
        numero = request.form['numero']
        asi_gan = request.form['asi_gan']
        gar_gan = request.form['gar_gan']
        med_gri = request.form['med_gri']
        obs = request.form['obs']
        vt = request.form['vt']
        pt = request.form['pt']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE frppr
            SET proc = %s,
                revis = %s,
                nivel_il = %s,
				con_sup = %s,
                met_insp = %s,
				tipo_il = %s,
                check1 = %s,
				check2 = %s,
                check3 = %s,
				detalle = %s,
                proc_p = %s,
				revis_p = %s,
                temp_ens = %s,
				tipo_il_p = %s,
                nivel_il_p = %s,
				mater_base = %s,
                tipo_sec = %s,
				tipo_pen = %s,
                marca_kit = %s,
				tiem_pen = %s,
                met_rem = %s,
				marca_kit1 = %s,
                tiem_sec = %s,
				for_rev = %s,
                marca_kit2 = %s,
				tiem_rev = %s,
                equipo = %s,
				marca = %s,
                iden = %s,
                marca_pas = %s,
                iden_pas = %s,
                modelo_pas = %s,
                capac_pas = %s,
                numero = %s,
                asi_gan = %s,
                gar_gan = %s,
                med_gri = %s,
                obs = %s,
                vt = %s,
                pt = %s
            WHERE id = %s
        """, (proc, revis, nivel_il, con_sup, met_insp, tipo_il, check1, check2, check3, detalle, proc_p, revis_p, temp_ens, tipo_il_p, nivel_il_p, mater_base, tipo_sec, tipo_pen, marca_kit, tiem_pen, met_rem, marca_kit1, tiem_sec, for_rev, marca_kit2, tiem_rev, equipo, marca, iden,marca_pas, iden_pas, modelo_pas, capac_pas, numero, asi_gan, gar_gan, med_gri, obs,vt,pt,id))
        flash('Contact Updated Successfully')
        mysql.connection.commit()
        return redirect(url_for('resum_frppr'))

@app.route('/resum_frppr')
@login_required
def resum_frppr():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select * from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    datos = cursor.fetchall()
    cursor.execute(
        "select num_rep from formulario where id_formulario = (select MAX(id_formulario) from formulario where llave_formulario = 'FR-INSP-061.04');")
    num_rep = cursor.fetchone()
    cursor.execute(
        "select * from frppr where id_formulario = (select MAX(b.id_formulario) from formulario a inner join frppr b on a.id_formulario = b.id_formulario);")
    datos1 = cursor.fetchall()
    cursor.execute(
        "select MAX(id) from frppr ;")
    data1 = cursor.fetchone()
    cursor.execute(
        "select descr from cat_form where codigo = 'FR-INSP-061.04';")
    cata = cursor.fetchone()
    print(data1)
    
    return render_template('resum_frppr.html', datos=datos,num_rep=num_rep,datos1=datos1, contact=data1[0],cata=cata)



@app.route('/genera_pdffrppr2')
@login_required
def genera_pdffrppr2():
    options = {
        'dpi': '300',
        'page-size': 'A4',
        # 'orientation': 'Landscape',
        'margin-top': '0mm',
        'margin-right': '20mm',
        'margin-bottom': '20mm',
        'margin-left': '10mm',
        'encoding': "UTF-8",
        #'grayscale': None,
        'outline-depth':3,
        # 'footer-center':'[page]',
        'footer-line': None,
        "enable-local-file-access": None,
    }
    path = r'C:/Ricardo/paginas_web/u30/aplicacion/static/css/'
    css = [path + 'style.css']

    path_wkhtmltopdf = r'C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe'
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select llave_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    nom_form = cursor.fetchone()
    cursor.execute(
        "select num_rep from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    num_rep = cursor.fetchone()
    cursor.execute(
        "select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_insp = cursor.fetchone()
    cursor.execute(
        "select fecha_emision_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_emi = cursor.fetchone()
    cursor.execute(
        "select fecha_expiracion_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_exp = cursor.fetchone()
    cursor.execute(
        "select lugar_ins_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    lugar = cursor.fetchone()
    cursor.execute(
        "select nom_inspe_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    inpe = cursor.fetchone()
    cursor.execute(
        "select * from frppr where id_formulario = (select MAX(id_formulario) from formulario);")
    datos1 = cursor.fetchall()
    cursor.execute(
        "select MAX(id) from frppr ;")
    data1 = cursor.fetchone()
    html = render_template('resum_frppr_1.html', datos=nom_form,num_rep=num_rep, fec1=fec_insp, fec2=fec_emi, fec3=fec_exp, lugar=lugar, inspector=inpe, datos1=datos1, contact=data1[0])
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    #pdfkit.from_file("aplicacion/templates/cert_for1.html", "index.pdf", options=options,configuration=config)
    pdfkit.from_string(html, "resum_frppr_1.pdf", options=options,configuration=config)
    #pdfkit.from_url("http://127.0.0.1:5000/cert_for1", "cert_for1.pdf",options=options,configuration=config)
    print("="*50)
    return redirect(url_for('cert_for11'))

@app.route('/reporte_fotofrppr')
@login_required
def reporte_fotofrppr():
    lista = []
    for file in listdir(app.root_path+"/static/img/subidas/frppr/"):
        lista.append(file)
    return render_template("reporte_fotofrppr.html", lista=lista)


@app.route('/upload_frppr', methods=['get', 'post'])
def upload_frppr():
    form = UploadForm()  # carga request.from y request.file
    if form.validate_on_submit():
        f = form.photo.data
        filename = secure_filename(f.filename)
        f.save(app.root_path+"/static/img/subidas/frppr/"+filename)
        foto = app.root_path+"/static/img/subidas/frppr/"+filename
        cursor = mysql.connection.cursor()
        cursor.execute(
            "select id from frppr where id = (select MAX(id) from frppr) ;")
        llave_form = cursor.fetchone()
        cursor.execute('insert into rep_foto_frppr (foto,id_f) VALUES (%s,%s)',
                    ( foto,llave_form))
        mysql.connection.commit()
        return redirect(url_for('inicio_fotofrppr'))
    return render_template('upload_frppr.html', form=form)

@app.route('/inicio_fotofrppr')
@login_required
def inicio_fotofrppr():
    lista = []
    for file in listdir(app.root_path+"/static/img/subidas/frppr/"):
        lista.append(file)
    return render_template("inicio_fotofrppr.html", lista=lista)


@app.route('/cert_for11', methods=['GET', 'POST'])
@login_required
def cert_for11():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select * from frppr where id_formulario = (select MAX(id_formulario) from formulario);")
    datafr = cursor.fetchall()
    cursor.execute(
        "select * from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    data = cursor.fetchall()
    return render_template('cert_for11.html', datafr=datafr, data=data)


@app.route('/genera_pdffrppr')
@login_required
def genera_pdffrppr():
    options = {
        'page-size': 'A4',
        # 'orientation': 'Landscape',
        'margin-top': '20mm',
        'margin-right': '20mm',
        'margin-bottom': '20mm',
        'margin-left': '20mm',
        'encoding': "UTF-8",
        'outline-depth':3,
        # 'footer-center':'[page]',
        'footer-line': None,
        "enable-local-file-access": None,
    }
    path_wkhtmltopdf = r'C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe'
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select * from frppr where id_formulario = (select MAX(id_formulario) from formulario);")
    datafr = cursor.fetchall()
    cursor.execute(
        "select * from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    data = cursor.fetchall()
    html = render_template('cert_for11.html', datafr=datafr, data=data)
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    #pdfkit.from_file("aplicacion/templates/cert_for1.html", "index.pdf", options=options,configuration=config)
    pdfkit.from_string(html, "cert_for11.pdf", options=options,configuration=config)
    print("="*50)
    return redirect(url_for('inicio'))


@app.route('/home_12', methods=['GET', 'POST'])
@login_required
def home_12():
    cursor = mysql.connection.cursor()
    cursor.execute("select nombre from articulos where id =16;")
    nom_form = cursor.fetchone()
    cursor.execute("select descripcion from articulos where id = 16;")
    nom_form1 = cursor.fetchone()
    form = datos_reporte()
    if form.validate_on_submit():
        cur = mysql.connection.cursor()
        cur.execute("select (sec+1) from cod_rep where id = 24;")
        sec = cur.fetchone()
        print(sec)
        cur.execute("""
                    UPDATE cod_rep
                    SET sec = %s
                        WHERE id = 24
                """, sec)
        mysql.connection.commit()
        empre = request.form['empresa']
        cur.execute(
            "select CONCAT(prefijo,LPAD(sec, 5, '0')) from cod_rep where id_for = 13;")
        num_rep = cur.fetchone()
        fecha_insp = request.form['fec_inpec']
        fecha_emi = request.form['fec_emision']
        fecha_exp = request.form['fec_expiracion']
        lugar_ins = request.form['lugar_inpec']
        nombre_ins = request.form['nom_inspec']
        cursor = mysql.connection.cursor()
        cursor.execute('insert into formulario (llave_formulario,num_rep,desc_formulario,fecha_inspec_formulario,fecha_emision_formulario,fecha_expiracion_formulario,lugar_ins_formulario,nom_inspe_formulario,empresa,cod_form) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                       (nom_form,num_rep, nom_form1, fecha_insp, fecha_emi, fecha_exp, lugar_ins, nombre_ins, empre,'frpau'))
        mysql.connection.commit()
        flash('Guardado Correctamente')
        datos = cursor.fetchone()
        print(datos)
        # return 'OK'
        return redirect(url_for('frpau'))
    return render_template('home_12.html', form=form, datos=nom_form, desc=nom_form1)


@app.route('/frpau', methods=['GET', 'POST'])
@login_required
def frpau():
    form = formu11()
    if form.validate_on_submit():
        revis = request.form['revis']
        nivel_il = request.form['nivel_il']
        con_sup = request.form['con_sup']
        met_insp = request.form['met_insp']
        tipo_il = request.form['tipo_il']
        check1 = request.form['check1']
        check2 = request.form['check2']
        check3 = request.form['check3']
        detalle = request.form['detalle']
        revis_p = request.form['revis_p']
        temp_ens = request.form['temp_ens']
        tipo_il_p = request.form['tipo_il_p']
        nivel_il_p = request.form['nivel_il_p']
        mater_base = request.form['mater_base']
        tipo_sec = request.form['tipo_sec']
        equipo = request.form['equipo']
        modelo = request.form['modelo']
        iden = request.form['iden']
        marca_pas = request.form['marca_pas']
        iden_pas = request.form['iden_pas']
        modelo_pas = request.form['modelo_pas']
        capac_pas = request.form['capac_pas']
        numero = request.form['numero']
        asi_gan = request.form['asi_gan']
        gar_gan = request.form['gar_gan']
        med_gri = request.form['med_gri']
        obs = request.form['obs']
        vt = request.form['vt']
        pt = request.form['pt']
        cur = mysql.connection.cursor()
        cur.execute(
            "select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
        llave_form = cur.fetchone()
        cur.execute(
            "select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
        fecha_form = cur.fetchone()
        cur.execute('insert into frppr (id_formulario,fec_formulario,proc,revis,nivel_il,con_sup,met_insp,tipo_il,check1,check2,check3,detalle,proc_p,revis_p,temp_ens,tipo_il_p,nivel_il_p,mater_base,tipo_sec,tipo_pen,marca_kit,tiem_pen,met_rem,marca_kit1,tiem_sec,for_rev,marca_kit2,tiem_rev,equipo,modelo,iden,marca_pas,iden_pas,modelo_pas,capac_pas,numero,asi_gan,gar_gan,med_gri,obs,vt,pt,tipo_pa) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                    (llave_form, fecha_form, 'PR-INSP-006', revis, nivel_il, con_sup, met_insp, tipo_il, check1, check2, check3, detalle, 'PR-INSP-007', revis_p, temp_ens, tipo_il_p, nivel_il_p, mater_base, tipo_sec, 'II VISIBLE', 'Met-L-Chek  VP-31A', '5 minutos', 'REMOVIBLE SOLVENTE', 'Met-L-Chek   E-59A', '10 minutos', 'SOLVENTE REMOVED', 'Met-L-Chek   D-70', '10 minutos', equipo, modelo, iden, marca_pas, iden_pas, modelo_pas, capac_pas, numero, asi_gan, gar_gan, med_gri, obs, vt, pt,'0' ))
        mysql.connection.commit()
        return redirect(url_for('resum_frppr'))

    return render_template('frpau.html', form=form)





@app.route('/cert_for12', methods=['GET', 'POST'])
@login_required
def cert_for12():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select marca_pas from frppr where id_formulario = (select MAX(id_formulario) from formulario);")
    marca_pas = cursor.fetchone()
    cursor.execute(
        "select modelo_pas from frppr  where id_formulario = (select MAX(id_formulario) from formulario);")
    modelo_pas = cursor.fetchone()
    cursor.execute(
        "select iden_pas from frppr where id_formulario = (select MAX(id_formulario) from formulario);")
    iden_pas = cursor.fetchone()
    cursor.execute(
        "select capac_pas from frppr where id_formulario = (select MAX(id_formulario) from formulario);")
    capac_pas = cursor.fetchone()
    cursor.execute(
        "select fecha_emision_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_emi = cursor.fetchone()
    cursor.execute(
        "select fecha_expiracion_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_exp = cursor.fetchone()
    return render_template('cert_for12.html', marca_pas=marca_pas, modelo_pas=modelo_pas, iden_pas=iden_pas, capac_pas=capac_pas, fec_emi=fec_emi, fec_exp=fec_exp)


@app.route('/genera_pdffrppr1')
@login_required
def genera_pdffrppr1():
    options = {
        'page-size': 'A4',
        # 'orientation': 'Landscape',
        'margin-top': '20mm',
        'margin-right': '20mm',
        'margin-bottom': '20mm',
        'margin-left': '20mm',
        'encoding': "UTF-8",
        'outline-depth':3,
        # 'footer-center':'[page]',
        'footer-line': None,
        "enable-local-file-access": None,
    }
    path_wkhtmltopdf = r'C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe'
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select marca_pas from frppr where id_formulario = (select MAX(id_formulario) from formulario);")
    marca_pas = cursor.fetchone()
    cursor.execute(
        "select modelo_pas from frppr  where id_formulario = (select MAX(id_formulario) from formulario);")
    modelo_pas = cursor.fetchone()
    cursor.execute(
        "select iden_pas from frppr where id_formulario = (select MAX(id_formulario) from formulario);")
    iden_pas = cursor.fetchone()
    cursor.execute(
        "select capac_pas from frppr where id_formulario = (select MAX(id_formulario) from formulario);")
    capac_pas = cursor.fetchone()
    cursor.execute(
        "select fecha_emision_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_emi = cursor.fetchone()
    cursor.execute(
        "select fecha_expiracion_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_exp = cursor.fetchone()
    html = render_template('cert_for12.html', marca_pas=marca_pas, modelo_pas=modelo_pas, iden_pas=iden_pas, capac_pas=capac_pas, fec_emi=fec_emi, fec_exp=fec_exp)
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    #pdfkit.from_file("aplicacion/templates/cert_for1.html", "index.pdf", options=options,configuration=config)
    pdfkit.from_string(html, "cert_for12.pdf", options=options,configuration=config)
    print("="*50)
    return redirect(url_for('inicio'))


@app.route('/home_13', methods=['GET', 'POST'])
@login_required
def home_13():
    cursor = mysql.connection.cursor()
    cursor.execute("select nombre from articulos where id = 17;")
    nom_form = cursor.fetchone()
    cursor.execute("select descripcion from articulos where id = 17;")
    nom_form1 = cursor.fetchone()
    form = datos_reporte()
    if form.validate_on_submit():
        cur = mysql.connection.cursor()
        cur.execute("select (sec+1) from cod_rep where id = 25;")
        sec = cur.fetchone()
        print(sec)
        cur.execute("""
                    UPDATE cod_rep
                    SET sec = %s
                        WHERE id = 25
                """, sec)
        mysql.connection.commit()
        empre = request.form['empresa']
        cur.execute(
            "select CONCAT(prefijo,LPAD(sec, 5, '0')) from cod_rep where id_for = 14;")
        num_rep = cur.fetchone()
        fecha_insp = request.form['fec_inpec']
        fecha_emi = request.form['fec_emision']
        fecha_exp = request.form['fec_expiracion']
        lugar_ins = request.form['lugar_inpec']
        nombre_ins = request.form['nom_inspec']
        cursor = mysql.connection.cursor()
        cursor.execute('insert into formulario (llave_formulario,num_rep,desc_formulario,fecha_inspec_formulario,fecha_emision_formulario,fecha_expiracion_formulario,lugar_ins_formulario,nom_inspe_formulario,empresa,cod_form) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                       (nom_form,num_rep, nom_form1, fecha_insp, fecha_emi, fecha_exp, lugar_ins, nombre_ins, empre,'frapa'))
        mysql.connection.commit()
        flash('Guardado Correctamente')
        datos = cursor.fetchone()
        print(datos)
        # return 'OK'
        return redirect(url_for('frapa'))
    return render_template('home_13.html', form=form, datos=nom_form, desc=nom_form1)


@app.route('/frapa', methods=['GET', 'POST'])
@login_required
def frapa():
    form = formu12()
    if form.validate_on_submit():
        revis = request.form['revis']
        nivel_il = request.form['nivel_il']
        con_sup = request.form['con_sup']
        met_insp = request.form['met_insp']
        tipo_il = request.form['tipo_il']
        check1 = request.form['check1']
        check2 = request.form['check2']
        check3 = request.form['check3']
        detalle = request.form['detalle']
        elem_ens = request.form['elem_ens']
        revis_p = request.form['revis_p']
        temp_ens = request.form['temp_ens']
        tipo_il_p = request.form['tipo_il_p']
        nivel_il_p = request.form['nivel_il_p']
        mater_base = request.form['mater_base']
        tipo_sec = request.form['tipo_sec']
        equipo = request.form['equipo']
        modelo = request.form['modelo']
        iden = request.form['iden']
        c1 = request.form['c1']
        c2 = request.form['c2']
        c3 = request.form['c3']
        c4 = request.form['c4']
        c5 = request.form['c5']
        c6 = request.form['c6']
        c7 = request.form['c7']
        c8 = request.form['c8']
        c9 = request.form['c9']
        c10 = request.form['c10']
        c11 = request.form['c11']
        c12 = request.form['c12']
        c13 = request.form['c13']
        c14 = request.form['c14']
        c15 = request.form['c15']
        c16 = request.form['c16']
        c17 = request.form['c17']
        c18 = request.form['c18']
        c19 = request.form['c19']
        c20 = request.form['c20']
        c21 = request.form['c21']
        cur = mysql.connection.cursor()
        cur.execute(
            "select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
        llave_form = cur.fetchone()
        cur.execute(
            "select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
        fecha_form = cur.fetchone()
        cur.execute('insert into frapa (id_formulario,fec_formulario,proc,revis,nivel_il,con_sup,met_insp,tipo_il,check1,check2,check3,detalle,elem_ens,proc_p,revis_p,temp_ens,tipo_il_p,nivel_il_p,mater_base,tipo_sec,tipo_pen,marca_kit,tiem_pen,met_rem,marca_kit1,tiem_sec,for_rev,marca_kit2,tiem_rev,equipo,modelo,iden,c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12,c13,c14,c15,c16,c17,c18,c19,c20,c21) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                    (llave_form, fecha_form, 'PR-INSP-006', revis, nivel_il, con_sup, met_insp, tipo_il, check1, check2, check3, detalle,elem_ens, 'PR-INSP-007', revis_p, temp_ens, tipo_il_p, nivel_il_p, mater_base, tipo_sec,  'II VISIBLE', 'Met-L-Chek  VP-31A', '5 minutos', 'REMOVIBLE SOLVENTE', 'Met-L-Chek   E-59A', '10 minutos', 'SOLVENTE REMOVED', 'Met-L-Chek   D-70', '10 minutos', equipo, modelo, iden, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13, c14, c15, c16, c17, c18, c19, c20, c21))
        mysql.connection.commit()
        return redirect(url_for('frapa1'))

    return render_template('frapa.html', form=form)




@app.route('/add_frapa1', methods=['POST'])
@login_required
def add_frapa1():
    form = formu12_1()
    cur = mysql.connection.cursor()
    cur.execute("select (sec+1) from codigo where id_for = 14;")
    sec = cur.fetchone()
    cur.execute("""
            UPDATE codigo
            SET sec = %s
                WHERE id = 14
        """, sec)
    mysql.connection.commit()
    if form.validate_on_submit():
        cur = mysql.connection.cursor()
        tipo_acc = request.form['tipo_acc']
        cur.execute("select CONCAT(preffijo,LPAD(sec, 5, '0')) from codigo where id_for = 14;")
        cod_enii = cur.fetchone()
        ref = request.form['ref']
        medidas = request.form['medidas']
        capac = request.form['capac']
        medida_cu = request.form['medida_cu']
        vt = request.form['vt']
        pt = request.form['pt']
        cur.execute("select id from frapa where id = (select MAX(id) from frapa) ;")
        llave_form = cur.fetchone()
        print(llave_form)
        cur.execute('insert into frapa1 (tipo_acc,ref,cod_enii,medidas,capac,medida_cu,vt,pt,id_f12) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                    (tipo_acc, ref, cod_enii, medidas, capac, medida_cu, vt, pt, llave_form))
        mysql.connection.commit()
        return redirect(url_for('frapa1'))



@app.route('/frapa1', methods=['GET', 'POST'])
@login_required
def frapa1():
    form = formu12_1()
    cur = mysql.connection.cursor()
    cur.execute("select * from frapa1 where id_f12=(select MAX(id) from frapa) ;")
    data = cur.fetchall()
    return render_template('frapa1.html', form=form, data=data)


@app.route('/edit_frapa/<id>', methods=['POST', 'GET'])
@login_required
def get_frapa(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM frapa WHERE id = %s', (id,))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-frapa.html', contact=data[0])



@app.route('/update_frapa/<id>', methods=['POST'])
@login_required
def update_frapa(id):
    if request.method == 'POST':
        proc = request.form['proc']
        revis = request.form['revis']
        nivel_il = request.form['nivel_il']
        con_sup = request.form['con_sup']
        met_insp = request.form['met_insp']
        tipo_il = request.form['tipo_il']
        check1 = request.form['check1']
        check2 = request.form['check2']
        check3 = request.form['check3']
        detalle = request.form['detalle']
        proc_p = request.form['proc_p']
        revis_p = request.form['revis_p']
        temp_ens = request.form['temp_ens']
        tipo_il_p = request.form['tipo_il_p']
        nivel_il_p = request.form['nivel_il_p']
        mater_base = request.form['mater_base']
        tipo_sec = request.form['tipo_sec']
        tipo_pen = request.form['tipo_pen']
        marca_kit = request.form['marca_kit']
        tiem_pen = request.form['tiem_pen']
        met_rem = request.form['met_rem']
        marca_kit1 = request.form['marca_kit1']
        tiem_sec = request.form['tiem_sec']
        for_rev = request.form['for_rev']
        marca_kit2 = request.form['marca_kit2']
        tiem_rev = request.form['tiem_rev']
        equipo = request.form['equipo']
        modelo = request.form['modelo']
        iden = request.form['iden']
        c1 = request.form['c1']
        c2 = request.form['c2']
        c3 = request.form['c3']
        c4 = request.form['c4']
        c5 = request.form['c5']
        c6 = request.form['c6']
        c7 = request.form['c7']
        c8 = request.form['c8']
        c9 = request.form['c9']
        c10 = request.form['c10']
        c11 = request.form['c11']
        c12 = request.form['c12']
        c13 = request.form['c13']
        c14 = request.form['c14']
        c15 = request.form['c15']
        c16 = request.form['c16']
        c17 = request.form['c17']
        c18 = request.form['c18']
        c19 = request.form['c19']
        c20 = request.form['c20']
        c21 = request.form['c21']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE frapa
            SET proc = %s,
                revis = %s,
                nivel_il = %s,
				con_sup = %s,
                met_insp = %s,
				tipo_il = %s,
                check1 = %s,
				check2 = %s,
                check3 = %s,
				detalle = %s,
                proc_p = %s,
                revis_p = %s,
                temp_ens = %s,
                tipo_il_p = %s,
                nivel_il_p = %s,
                mater_base = %s,
                tipo_sec = %s,
                tipo_pen = %s,
                marca_kit = %s,
                tiem_pen = %s,
                met_rem = %s,
                marca_kit1 = %s,
                tiem_sec = %s,
                for_rev = %s,
                marca_kit2 = %s,
                tiem_rev = %s,
                equipo = %s,
                modelo = %s,
                iden = %s,
                c1 = %s,
                c2 = %s,
                c3 = %s,
                c4 = %s,
                c5 = %s,
                c6 = %s,
                c7 = %s,
                c8 = %s,
                c9 = %s,
                c10 = %s,
                c11 = %s,
                c12 = %s,
                c13 = %s,
                c14 = %s,
                c15 = %s,
                c16 = %s,
                c17 = %s,
                c18 = %s,
                c19 = %s,
                c20 = %s,
                c21 = %s
            WHERE id = %s
        """, (proc, revis, nivel_il, con_sup, met_insp, tipo_il, check1, check2, check3, detalle,proc_p,revis_p,temp_ens,tipo_il_p,nivel_il_p,mater_base,tipo_sec,tipo_pen,marca_kit,tiem_pen,met_rem, marca_kit1,tiem_sec,for_rev,marca_kit2,tiem_rev,equipo, modelo, iden,c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12,c13,c14,c15,c16,c17,c18,c19,c20,c21, id))
        flash('Contact Updated Successfully')
        mysql.connection.commit()
        return redirect(url_for('resum_frapa'))



@app.route('/edit-frapa1/<id>', methods=['POST', 'GET'])
@login_required
def get_frapa1(id):
    cur = mysql.connection.cursor()
    cur.execute(
        'SELECT * FROM frapa1 WHERE num = %s and id_f12 = (select MAX(id) from frapa)', (id,))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-frapa1.html', contact=data[0])


       

@app.route('/update_frapa1/<id>', methods=['POST'])
@login_required
def update_frapa1(id):
    if request.method == 'POST':
        num = request.form['num']
        ref = request.form['ref']
        cod_enii = request.form['cod_enii']
        medidas = request.form['medidas']
        capac = request.form['capac']
        medida_cu = request.form['medida_cu']
        tipo_acc = request.form['tipo_acc']
        vt = request.form['vt']
        pt = request.form['pt']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE frapa1
            SET num = %s,
                ref = %s, 
                cod_enii = %s,
                medidas = %s,
                capac = %s,
                medida_cu = %s,
                tipo_acc = %s,
				vt = %s,
                pt = %s
            WHERE num = %s
        """, (num,ref, cod_enii, medidas, capac,medida_cu,tipo_acc, vt, pt, num))
        flash('Contact Updated Successfully')
        mysql.connection.commit()
        return redirect(url_for('frapa1'))


@app.route('/resum_frapa')
@login_required
def resum_frapa():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select * from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    datos = cursor.fetchall()
    cursor.execute(
        "select num_rep from formulario where id_formulario = (select MAX(b.id_formulario) from formulario a inner join frapa b on a.id_formulario = b.id_formulario);")
    num_rep = cursor.fetchone()
    cursor.execute(
        "select * from frapa where id_formulario = (select MAX(b.id_formulario) from formulario a inner join frapa b on a.id_formulario = b.id_formulario);")
    datos1 = cursor.fetchall()
    cursor.execute(
        "select MAX(id) from frapa ;")
    data1 = cursor.fetchone()
    cursor.execute(
        "select * from frapa1 where id_f12 = (select MAX(id) from frapa) ;")
    data = cursor.fetchall()
    cursor.execute(
        "select descr from cat_form where codigo = 'FR-INSP-065.02';")
    cata = cursor.fetchone()
    print(data)
    return render_template('resum_frapa.html', datos=datos,num_rep=num_rep,datos1=datos1, contact=data1[0], data=data,cata=cata)


@app.route('/genera_pdffrapa2')
@login_required
def genera_pdffrapa2():
    options = {
        'dpi': '300',
        'page-size': 'A4',
        # 'orientation': 'Landscape',
        'margin-top': '0mm',
        'margin-right': '20mm',
        'margin-bottom': '20mm',
        'margin-left': '10mm',
        'encoding': "UTF-8",
        #'grayscale': None,
        'outline-depth':3,
        # 'footer-center':'[page]',
        'footer-line': None,
        "enable-local-file-access": None,
    }
    path = r'C:/Ricardo/paginas_web/u30/aplicacion/static/css/'
    css = [path + 'style.css']

    path_wkhtmltopdf = r'C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe'
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select llave_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    nom_form = cursor.fetchone()
    cursor.execute(
        "select num_rep from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    num_rep = cursor.fetchone()
    cursor.execute(
        "select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_insp = cursor.fetchone()
    cursor.execute(
        "select fecha_emision_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_emi = cursor.fetchone()
    cursor.execute(
        "select fecha_expiracion_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_exp = cursor.fetchone()
    cursor.execute(
        "select lugar_ins_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    lugar = cursor.fetchone()
    cursor.execute(
        "select nom_inspe_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    inpe = cursor.fetchone()
    cursor.execute(
        "select * from frapa where id_formulario = (select MAX(id_formulario) from formulario);")
    datos1 = cursor.fetchall()
    cursor.execute(
        "select MAX(id) from frapa ;")
    data1 = cursor.fetchone()
    cursor.execute(
        "select * from frapa1 where id_f12 = (select MAX(id) from frapa) ;")
    data = cursor.fetchall()
    html = render_template('resum_frapa_1.html', datos=nom_form,num_rep=num_rep, fec1=fec_insp, fec2=fec_emi, fec3=fec_exp, lugar=lugar, inspector=inpe, datos1=datos1, contact=data1[0], data=data)
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    #pdfkit.from_file("aplicacion/templates/cert_for1.html", "index.pdf", options=options,configuration=config)
    pdfkit.from_string(html, "resum_frapa_1.pdf", options=options,configuration=config)
    #pdfkit.from_url("http://127.0.0.1:5000/cert_for1", "cert_for1.pdf",options=options,configuration=config)
    print("="*50)
    return redirect(url_for('cert_for13'))

@app.route('/reporte_fotofrapa')
@login_required
def reporte_fotofrapa():
    lista = []
    for file in listdir(app.root_path+"/static/img/subidas/frapa/"):
        lista.append(file)
    return render_template("reporte_fotofrapa.html", lista=lista)


@app.route('/upload_frapa', methods=['get', 'post'])
def upload_frapa():
    form = UploadForm()  # carga request.from y request.file
    if form.validate_on_submit():
        f = form.photo.data
        filename = secure_filename(f.filename)
        f.save(app.root_path+"/static/img/subidas/frapa/"+filename)
        foto = app.root_path+"/static/img/subidas/frapa/"+filename
        cursor = mysql.connection.cursor()
        cursor.execute(
            "select id from frapa where id = (select MAX(id) from frapa) ;")
        llave_form = cursor.fetchone()
        cursor.execute('insert into rep_foto_frapa (foto,id_f) VALUES (%s,%s)',
                    ( foto,llave_form))
        mysql.connection.commit()
        return redirect(url_for('inicio_fotofrapa'))
    return render_template('upload_frapa.html', form=form)

@app.route('/inicio_fotofrapa')
@login_required
def inicio_fotofrapa():
    lista = []
    for file in listdir(app.root_path+"/static/img/subidas/frapa/"):
        lista.append(file)
    return render_template("inicio_fotofrapa.html", lista=lista)
    

@app.route('/cert_for13', methods=['GET', 'POST'])
@login_required
def cert_for13():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select * from frapa1 where id_f12 = (select MAX(id) from frapa);")
    datafr = cursor.fetchall()
    cursor.execute(
        "select * from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    data = cursor.fetchall()
    return render_template('cert_for13.html', datafr=datafr, data=data)


@app.route('/genera_pdffrapa')
@login_required
def genera_pdffrapa():
    options = {
        'page-size': 'A4',
        # 'orientation': 'Landscape',
        'margin-top': '20mm',
        'margin-right': '20mm',
        'margin-bottom': '20mm',
        'margin-left': '20mm',
        'encoding': "UTF-8",
        'outline-depth':3,
        # 'footer-center':'[page]',
        'footer-line': None,
        "enable-local-file-access": None,
    }
    path_wkhtmltopdf = r'C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe'
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select * from frapa1 where id_f12 = (select MAX(id) from frapa);")
    datafr = cursor.fetchall()
    cursor.execute(
        "select * from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    data = cursor.fetchall()
    html = render_template('cert_for13.html', datafr=datafr, data=data)
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    #pdfkit.from_file("aplicacion/templates/cert_for1.html", "index.pdf", options=options,configuration=config)
    pdfkit.from_string(html, "cert_for13.pdf", options=options,configuration=config)
    print("="*50)
    return redirect(url_for('inicio'))


@app.route('/home_14', methods=['GET', 'POST'])
@login_required
def home_14():
    cursor = mysql.connection.cursor()
    cursor.execute("select nombre from articulos where id = 18;")
    nom_form = cursor.fetchone()
    cursor.execute("select descripcion from articulos where id = 18;")
    nom_form1 = cursor.fetchone()
    form = datos_reporte()
    if form.validate_on_submit():
        cur = mysql.connection.cursor()
        cur.execute("select (sec+1) from cod_rep where id = 26;")
        sec = cur.fetchone()
        print(sec)
        cur.execute("""
                    UPDATE cod_rep
                    SET sec = %s
                        WHERE id = 26
                """, sec)
        mysql.connection.commit()
        empre = request.form['empresa']
        cur.execute(
            "select CONCAT(prefijo,LPAD(sec, 5, '0')) from cod_rep where id_for = 15;")
        num_rep = cur.fetchone()
        fecha_insp = request.form['fec_inpec']
        fecha_emi = request.form['fec_emision']
        fecha_exp = request.form['fec_expiracion']
        lugar_ins = request.form['lugar_inpec']
        nombre_ins = request.form['nom_inspec']
        cursor = mysql.connection.cursor()
        cursor.execute('insert into formulario (llave_formulario,num_rep,desc_formulario,fecha_inspec_formulario,fecha_emision_formulario,fecha_expiracion_formulario,lugar_ins_formulario,nom_inspe_formulario,empresa,cod_form) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                       (nom_form,num_rep, nom_form1, fecha_insp, fecha_emi, fecha_exp, lugar_ins, nombre_ins, empre,'frttr'))
        mysql.connection.commit()
        flash('Guardado Correctamente')
        datos = cursor.fetchone()
        print(datos)
        # return 'OK'
        return redirect(url_for('frttr'))
    return render_template('home_14.html', form=form, datos=nom_form, desc=nom_form1)


@app.route('/frttr', methods=['GET', 'POST'])
@login_required
def frttr():
    form = formu13()
    if form.validate_on_submit():
        revis = request.form['revis']
        nivel_il = request.form['nivel_il']
        con_sup = request.form['con_sup']
        met_insp = request.form['met_insp']
        tipo_il = request.form['tipo_il']
        check1 = request.form['check1']
        check2 = request.form['check2']
        check3 = request.form['check3']
        detalle = request.form['detalle']
        ele_ens = request.form['ele_ens']
        revis_p = request.form['revis_p']
        temp_ens = request.form['temp_ens']
        tipo_il_p = request.form['tipo_il_p']
        nivel_il_p = request.form['nivel_il_p']
        mater_base = request.form['mater_base']
        tipo_sec = request.form['tipo_sec']
        equipo = request.form['equipo']
        modelo = request.form['modelo']
        iden = request.form['iden']
        cur = mysql.connection.cursor()
        cur.execute(
            "select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
        llave_form = cur.fetchone()
        cur.execute(
            "select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
        fecha_form = cur.fetchone()
        cur.execute('insert into frttr (id_formulario,fec_formulario,proc,revis,nivel_il,con_sup,met_insp,tipo_il,check1,check2,check3,detalle,ele_ens,proc_p,revis_p,temp_ens,tipo_il_p,nivel_il_p,mater_base,tipo_sec,tipo_pen,marca_kit,tiem_pen,met_rem,marca_kit1,tiem_sec,for_rev,marca_kit2,tiem_rev,equipo,modelo,iden) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                    (llave_form, fecha_form, 'PR-INSP-006', revis, nivel_il, con_sup, met_insp, tipo_il, check1, check2, check3, detalle, 'PR-INSP-007', ele_ens,revis_p, temp_ens, tipo_il_p, nivel_il_p, mater_base, tipo_sec,'II VISIBLE', 'Met-L-Chek  VP-31A', '5 minutos', 'REMOVIBLE SOLVENTE', 'Met-L-Chek   E-59A', '10 minutos', 'SOLVENTE REMOVED', 'Met-L-Chek   D-70', '10 minutos' , equipo, modelo, iden))
        mysql.connection.commit()
        return redirect(url_for('frttr1'))

    return render_template('frttr.html', form=form)


@app.route('/add_frttr1', methods=['POST'])
@login_required
def add_frttr1():
    form = formu13_1()
    cur = mysql.connection.cursor()
    cur.execute("select (sec+1) from codigo where id_for = 15;")
    sec = cur.fetchone()
    cur.execute("""
            UPDATE codigo
            SET sec = %s
                WHERE id = 15
        """, sec)
    mysql.connection.commit()
    if form.validate_on_submit():
        ref = request.form['ref']
        cur.execute(
            "select CONCAT(preffijo,LPAD(sec, 5, '0')) from codigo where id_for = 15;")
        cod_enii = cur.fetchone()
        medidas = request.form['medidas']
        capac = request.form['capac']
        gancho1 = request.form['gancho1']
        gancho2 = request.form['gancho2']
        vt = request.form['vt']
        pt = request.form['pt']
        cur = mysql.connection.cursor()
        cur.execute(
            "select id from frttr where id = (select MAX(id) from frttr) ;")
        llave_form = cur.fetchone()
        print(llave_form)
        cur.execute('insert into frttr1 (ref,cod_enii,medidas,capac,gancho1,gancho2,vt,pt,id_f13) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                    (ref, cod_enii, medidas, capac, gancho1, gancho2, vt, pt, llave_form))
        mysql.connection.commit()
        return redirect(url_for('frttr1'))



@app.route('/frttr1', methods=['GET', 'POST'])
@login_required
def frttr1():
    form = formu13_1()
    cur = mysql.connection.cursor()
    cur.execute("select * from frttr1 where id_f13=(select MAX(id) from frttr) ;")
    data = cur.fetchall()
    return render_template('frttr1.html', form=form, data=data)


@app.route('/edit_frttr/<id>', methods=['POST', 'GET'])
@login_required
def get_frttr(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM frttr WHERE id = %s', (id,))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-frttr.html', contact=data[0])


@app.route('/update_frttr/<id>', methods=['POST'])
@login_required
def update_frttr(id):
    if request.method == 'POST':
        proc = request.form['proc']
        revis = request.form['revis']
        nivel_il = request.form['nivel_il']
        con_sup = request.form['con_sup']
        met_insp = request.form['met_insp']
        tipo_il = request.form['tipo_il']
        check1 = request.form['check1']
        check2 = request.form['check2']
        check3 = request.form['check3']
        detalle = request.form['detalle']
        ele_ens = request.form['ele_ens']
        proc_p = request.form['proc_p']
        revis_p = request.form['revis_p']
        temp_ens = request.form['temp_ens']
        tipo_il_p = request.form['tipo_il_p']
        nivel_il_p = request.form['nivel_il_p']
        mater_base = request.form['mater_base']
        tipo_sec = request.form['tipo_sec']
        tipo_pen = request.form['tipo_pen']
        marca_kit = request.form['marca_kit']
        tiem_pen = request.form['tiem_pen']
        met_rem = request.form['met_rem']
        marca_kit1 = request.form['marca_kit1']
        tiem_sec = request.form['tiem_sec']
        for_rev = request.form['for_rev']
        marca_kit2 = request.form['marca_kit2']
        tiem_rev = request.form['tiem_rev']
        equipo = request.form['equipo']
        modelo = request.form['modelo']
        iden = request.form['iden']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE frttr
            SET proc = %s,
                revis = %s,
                nivel_il = %s,
				con_sup = %s,
                met_insp = %s,
				tipo_il = %s,
                check1 = %s,
				check2 = %s,
                check3 = %s,
				detalle = %s,
				ele_ens = %s,
                proc_p = %s,
				revis_p = %s,
                temp_ens = %s,
				tipo_il_p = %s,
                nivel_il_p = %s,
				mater_base = %s,
                tipo_sec = %s,
				tipo_pen = %s,
                marca_kit = %s,
				tiem_pen = %s,
                met_rem = %s,
				marca_kit1 = %s,
                tiem_sec = %s,
				for_rev = %s,
                marca_kit2 = %s,
				tiem_rev = %s,
                equipo = %s,
				modelo = %s,
                iden = %s
            WHERE id = %s
        """, (proc, revis, nivel_il, con_sup, met_insp, tipo_il, check1, check2, check3, detalle, ele_ens, proc_p, revis_p, temp_ens, tipo_il_p, nivel_il_p, mater_base, tipo_sec, tipo_pen, marca_kit, tiem_pen, met_rem, marca_kit1, tiem_sec, for_rev, marca_kit2, tiem_rev, equipo, modelo, iden, id))
        flash('Contact Updated Successfully')
        mysql.connection.commit()
        return redirect(url_for('resum_frttr'))


@app.route('/edit_frttr1/<id>', methods=['POST', 'GET'])
@login_required
def get_frttr1(id):
    cur = mysql.connection.cursor()
    cur.execute(
        'SELECT * FROM frttr1 WHERE num = %s and id_f13=(select MAX(id) from frttr)',  [id])
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-frttr1.html', contact=data[0])


@app.route('/update_frttr1/<id>', methods=['POST'])
@login_required
def update_frttr1(id):
    if request.method == 'POST':
        num = request.form['num']
        ref = request.form['ref']
        cod_enii = request.form['cod_enii']
        medidas = request.form['medidas']
        capac = request.form['capac']
        gancho1 = request.form['gancho1']
        gancho2 = request.form['gancho2']
        vt = request.form['vt']
        pt = request.form['pt']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE frttr1
            SET num = %s,
                ref = %s,
                cod_enii = %s,
				medidas = %s,
                capac = %s,
				gancho1 = %s,
				gancho2 = %s,
                vt = %s,
				pt = %s
            WHERE num = %s
        """, (num, ref, cod_enii,  medidas, capac, gancho1, gancho2, vt, pt, num))
        flash('Contact Updated Successfully')
        mysql.connection.commit()
        return redirect(url_for('frttr1'))

@app.route('/resum_frttr')
@login_required
def resum_frttr():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select * from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    datos = cursor.fetchone()
    cursor.execute(
        "select num_rep from formulario where id_formulario = (select MAX(b.id_formulario) from formulario a inner join frttr b on a.id_formulario = b.id_formulario);")
    num_rep = cursor.fetchone()
    cursor.execute(
        "select * from frttr where id_formulario = (select MAX(b.id_formulario) from formulario a inner join frttr b on a.id_formulario = b.id_formulario);")
    datos1 = cursor.fetchall()
    cursor.execute(
        "select MAX(id) from frttr ;")
    data1 = cursor.fetchone()
    cursor.execute(
        "select * from frttr1 where id_f13 = (select MAX(id) from frttr) ;")
    data = cursor.fetchall()
    cursor.execute(
        "select descr from cat_form where codigo = 'FR-INSP-066.00';")
    cata = cursor.fetchone()
    print(data)
    return render_template('resum_frttr.html', datos=datos,num_rep=num_rep,datos1=datos1, contact=data1[0], data=data,cata=cata)



@app.route('/genera_pdffrttr2')
@login_required
def genera_pdffrttr2():
    options = {
        'dpi': '300',
        'page-size': 'A4',
        # 'orientation': 'Landscape',
        'margin-top': '0mm',
        'margin-right': '20mm',
        'margin-bottom': '20mm',
        'margin-left': '10mm',
        'encoding': "UTF-8",
        #'grayscale': None,
        'outline-depth':3,
        # 'footer-center':'[page]',
        'footer-line': None,
        "enable-local-file-access": None,
    }
    path = r'C:/Ricardo/paginas_web/u30/aplicacion/static/css/'
    css = [path + 'style.css']

    path_wkhtmltopdf = r'C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe'
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select llave_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    nom_form = cursor.fetchone()
    cursor.execute(
        "select num_rep from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    num_rep = cursor.fetchone()
    cursor.execute(
        "select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_insp = cursor.fetchone()
    cursor.execute(
        "select fecha_emision_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_emi = cursor.fetchone()
    cursor.execute(
        "select fecha_expiracion_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_exp = cursor.fetchone()
    cursor.execute(
        "select lugar_ins_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    lugar = cursor.fetchone()
    cursor.execute(
        "select nom_inspe_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    inpe = cursor.fetchone()
    cursor.execute(
        "select * from frttr where id_formulario = (select MAX(id_formulario) from formulario);")
    datos1 = cursor.fetchall()
    cursor.execute(
        "select MAX(id) from frttr ;")
    data1 = cursor.fetchone()
    cursor.execute(
        "select * from frttr1 where id_f13 = (select MAX(id) from frttr) ;")
    data = cursor.fetchall()
    html = render_template('resum_frttr_1.html', datos=nom_form,num_rep=num_rep, fec1=fec_insp, fec2=fec_emi, fec3=fec_exp, lugar=lugar, inspector=inpe, datos1=datos1, contact=data1[0], data=data)
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    #pdfkit.from_file("aplicacion/templates/cert_for1.html", "index.pdf", options=options,configuration=config)
    pdfkit.from_string(html, "resum_frttr_1.pdf", options=options,configuration=config)
    #pdfkit.from_url("http://127.0.0.1:5000/cert_for1", "cert_for1.pdf",options=options,configuration=config)
    print("="*50)
    return redirect(url_for('cert_for14'))

@app.route('/reporte_fotofrttr')
@login_required
def reporte_fotofrttr():
    lista = []
    for file in listdir(app.root_path+"/static/img/subidas/frttr/"):
        lista.append(file)
    return render_template("reporte_fotofrttr.html", lista=lista)




@app.route('/upload_frttr', methods=['get', 'post'])
def upload_frttr():
    form = UploadForm()  # carga request.from y request.file
    if form.validate_on_submit():
        f = form.photo.data
        filename = secure_filename(f.filename)
        f.save(app.root_path+"/static/img/subidas/frttr/"+filename)
        foto = app.root_path+"/static/img/subidas/frttr/"+filename
        cursor = mysql.connection.cursor()
        cursor.execute(
            "select id from frttr where id = (select MAX(id) from frttr) ;")
        llave_form = cursor.fetchone()
        cursor.execute('insert into rep_foto_frttr (foto,id_f) VALUES (%s,%s)',
                    ( foto,llave_form))
        mysql.connection.commit()
        return redirect(url_for('inicio_fotofrttr'))
    return render_template('upload_frttr.html', form=form)

@app.route('/inicio_fotofrttr')
@login_required
def inicio_fotofrttr():
    lista = []
    for file in listdir(app.root_path+"/static/img/subidas/frttr/"):
        lista.append(file)
    return render_template("inicio_fotofrttr.html", lista=lista)

@app.route('/cert_for14', methods=['GET', 'POST'])
@login_required
def cert_for14():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select * from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    data = cursor.fetchall()
    cursor.execute(
        "select * from frttr1 where id_f13 = (select MAX(id) from frttr) ;")
    datafr = cursor.fetchall()

    return render_template('cert_for14.html', datafr=datafr, data=data)

@app.route('/genera_pdffrttr')
@login_required
def genera_pdffrttr():
    options = {
        'page-size': 'A4',
        # 'orientation': 'Landscape',
        'margin-top': '20mm',
        'margin-right': '20mm',
        'margin-bottom': '20mm',
        'margin-left': '20mm',
        'encoding': "UTF-8",
        'outline-depth':3,
        # 'footer-center':'[page]',
        'footer-line': None,
        "enable-local-file-access": None,
    }
    path_wkhtmltopdf = r'C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe'
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select * from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    data = cursor.fetchall()
    cursor.execute(
        "select * from frttr1 where id_f13 = (select MAX(id) from frttr) ;")
    datafr = cursor.fetchall()
    html = render_template('cert_for14.html', datafr=datafr, data=data)
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    #pdfkit.from_file("aplicacion/templates/cert_for1.html", "index.pdf", options=options,configuration=config)
    pdfkit.from_string(html, "cert_for14.pdf", options=options,configuration=config)
    print("="*50)
    return redirect(url_for('inicio'))

@app.route('/resumen')
@login_required
def resumen():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select llave_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    nom_form = cursor.fetchone()
    cursor.execute(
        "select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_insp = cursor.fetchone()
    cursor.execute(
        "select fecha_emision_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_emi = cursor.fetchone()
    cursor.execute(
        "select fecha_expiracion_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_exp = cursor.fetchone()
    cursor.execute(
        "select lugar_ins_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    lugar = cursor.fetchone()
    cursor.execute(
        "select nom_inspe_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    inpe = cursor.fetchone()
    return render_template('resumen.html', datos=nom_form, fec1=fec_insp, fec2=fec_emi, fec3=fec_exp, lugar=lugar, inspector=inpe)


@app.route('/caratula', methods=['GET', 'POST'])
@login_required
def caratula():
    form = datos_equipo()
    if form.validate_on_submit():
        marca = request.form['de_marca']
        serie = request.form['de_serie']
        tipo = request.form['de_tipo']
        modelo = request.form['de_modelo']
        capacidad = request.form['de_capacidad']
        kilometraje = request.form['de_kilometraje']
        anio = request.form['de_anio']
        codigo = request.form['de_cod_interno']
        marca_dm = request.form['dm_marca']
        serie_dm = request.form['dm_serie']
        modelo_dm = request.form['dm_modelo']
        horometro_dm = request.form['dm_horometro']
        ct_capmax = request.form['ct_capmax']
        ct_longpluma = request.form['ct_longpluma']
        ct_radio = request.form['ct_radio']
        ct_angulo = request.form['ct_angulo']
        ct_lmi = request.form['ct_lmi']
        ct_marca = request.form['ct_marca']
        ct_modelo = request.form['ct_modelo']
        ct_serie = request.form['ct_serie']
        pp_marca = request.form['pp_marca']
        pp_capacidad = request.form['pp_capacidad']
        pp_modelo = request.form['pp_modelo']
        pp_serie_ref = request.form['pp_serie_ref']
        pp_diam_clab = request.form['pp_diam_clab']
        ps_marca = request.form['ps_marca']
        ps_capacidad = request.form['ps_capacidad']
        ps_modelo = request.form['ps_modelo']
        ps_serieref = request.form['ps_serieref']
        ps_diam_clab = request.form['ps_diam_clab']
        cur = mysql.connection.cursor()
        cur.execute(
            "select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
        llave_form = cur.fetchone()
        cur.execute(
            "select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
        fecha_form = cur.fetchone()
        cur.execute('insert into datos_equipo (id_formulario,fec_formulario,MARCA_datos_equipo,serie_datos_equipo,tipo_datos_equipo,modelo_datos_equipo,cap_datos_equipo,km_datos_equipo,anio_datos_equipo,codint_datos_equipo) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                    (llave_form, fecha_form, marca, serie, tipo, modelo, capacidad, kilometraje, anio, codigo))
        cur.execute('insert into datos_motor (id_formulario,fec_formulario,MARCA_Datos_Motor,SERIE_Datos_Motor,MODELO_Datos_Motor,HOROMETRO_Datos_Motor) VALUES (%s,%s,%s,%s,%s,%s)',
                    (llave_form, fecha_form, marca_dm, serie_dm, modelo_dm, horometro_dm))
        cur.execute('insert into capacidad_trabajo (id_formulario,fec_formulario,CAP_MAX_Capacidad_Trabajo,LONG_PLUMA_Capacidad_Trabajo,RADIO_Capacidad_Trabajo,ANGULO_Capacidad_Trabajo) VALUES (%s,%s,%s,%s,%s,%s)',
                    (llave_form, fecha_form, ct_capmax, ct_longpluma, ct_radio, ct_angulo))
        cur.execute('insert into datos_lmi (id_formulario,fec_formulario,FABRICANTE_DATOS_LMI,MARCA_DATOS_LMI,MODELO_DATOS_LMI,SERIE_DATOS_LMI) VALUES (%s,%s,%s,%s,%s,%s)',
                    (llave_form, fecha_form, ct_lmi, ct_marca, ct_modelo, ct_serie))
        cur.execute('insert into pasteca_pri (id_formulario,fec_formulario,marca_pasteca_pri,capacidad_pasteca_pri,modelo_pasteca_pri,serie_ref_pasteca_pri,diacab_pasteca_pri) VALUES (%s,%s,%s,%s,%s,%s,%s)',
                    (llave_form, fecha_form, pp_marca, pp_capacidad, pp_modelo, pp_serie_ref, pp_diam_clab))
        cur.execute('insert into pasteca_sec (id_formulario,fec_formulario,marca_pasteca_sec,capacidad_pasteca_sec,modelo_pasteca_sec,serie_ref_pasteca_sec,diacab_pasteca_sec) VALUES (%s,%s,%s,%s,%s,%s,%s)',
                    (llave_form, fecha_form, ps_marca, ps_capacidad, ps_modelo, ps_serieref, ps_diam_clab))
        mysql.connection.commit()
        return render_template('CHECK_LIST_bck.html')
    return render_template('caratula.html', form=form)


@app.route('/CHECK_LIST', methods=['GET', 'POST'])
@login_required
def CHECK_LIST_bck():

    return render_template('CHECK_LIST_bck.html')


@app.route('/check1', methods=['GET', 'POST'])
@login_required
def check1():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    llave_form = cursor.fetchone()
    cursor.execute(
        "select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    fecha_form = cursor.fetchone()
    form = check_list1()
    if form.validate_on_submit():
        valor = request.form.get('micheck')
        if valor == '7':
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Matricula Doc Identificación'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Manual de Operación'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Manual de servicio-partes'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Programa de Mantenimiento'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Registros de Reparaciones'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Tablas de Carga'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'File de certificaciones'))
            mysql.connection.commit()
            return redirect(url_for('check2'))
        else:
            check1 = Text(form.check1.data)
            check2 = Text(form.check2.data)
            check3 = Text(form.check3.data)
            check4 = Text(form.check4.data)
            check5 = Text(form.check5.data)
            check6 = Text(form.check6.data)
            check7 = Text(form.check7.data)
            checkobs = Text(form.checkobs.data)
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check1, 'Matricula Doc Identificación', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check2, 'Manual de Operación', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check3, 'Manual de servicio-partes', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check4, 'Programa de Mantenimiento', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check5, 'Registros de Reparaciones', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check6, 'Tablas de Carga', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check7, 'File de certificaciones', checkobs))
            mysql.connection.commit()
            return redirect(url_for('check2'))
    return render_template('check1.html', dato=llave_form, form=form)


@app.route('/check2', methods=['GET', 'POST'])
@login_required
def check2():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    llave_form = cursor.fetchone()
    cursor.execute(
        "select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    fecha_form = cursor.fetchone()
    form = check_list2()
    if form.validate_on_submit():
        valor = request.form.get('micheck')
        if valor == '9':
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Accesos y puntos de apoyo, estado'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Puerta seguro posic. abierto y posic. cerrado'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Identificación de instrumentos y mandos'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Tipo de vidrio, parabrisas y techo'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Limpia parabrisas'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Cartilla de advertencia riesgo electrocución'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Estado de asiento, bloqueo posa brazo'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Cinturón de seguridad'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Condición de la cabina/estructura'))
            mysql.connection.commit()
            return redirect(url_for('check3'))
        else:
            check1 = Text(form.check1.data)
            check2 = Text(form.check2.data)
            check3 = Text(form.check3.data)
            check4 = Text(form.check4.data)
            check5 = Text(form.check5.data)
            check6 = Text(form.check6.data)
            check7 = Text(form.check7.data)
            check8 = Text(form.check7.data)
            check9 = Text(form.check7.data)
            checkobs = Text(form.checkobs.data)
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check1, 'Accesos y puntos de apoyo, estado', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check2, 'Puerta seguro posic. abierto y posic. cerrado', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check3, 'Identificación de instrumentos y mandos', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check4, 'Tipo de vidrio, parabrisas y techo', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check5, 'Limpia parabrisas', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check6, 'Cartilla de advertencia riesgo electrocución', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check7, 'Estado de asiento, bloqueo posa brazo', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check8, 'Cinturón de seguridad', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check9, 'Condición de la cabina/estructura', checkobs))
            mysql.connection.commit()
            return redirect(url_for('check3'))
    return render_template('check2.html', dato=llave_form, form=form)


@app.route('/check3', methods=['GET', 'POST'])
@login_required
def check3():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    llave_form = cursor.fetchone()
    cursor.execute(
        "select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    fecha_form = cursor.fetchone()
    form = check_list3()
    if form.validate_on_submit():
        valor = request.form.get('micheck')
        if valor == '5':
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Accesos y puntos de apoyo, estado'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Puerta seguro posic. abierto y posic. cerrado'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Identificación de instrumentos y mandos'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Tipo de vidrio, parabrisas y techo'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Limpia parabrisas'))
            mysql.connection.commit()
            return redirect(url_for('check4'))
        else:
            check1 = Text(form.check1.data)
            check2 = Text(form.check2.data)
            check3 = Text(form.check3.data)
            check4 = Text(form.check4.data)
            check5 = Text(form.check5.data)
            checkobs = Text(form.checkobs.data)
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check1, 'Accesos y puntos de apoyo, estado', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check2, 'Puerta seguro posic. abierto y posic. cerrado', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check3, 'Identificación de instrumentos y mandos', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check4, 'Tipo de vidrio, parabrisas y techo', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check5, 'Limpia parabrisas', checkobs))
            mysql.connection.commit()
            return redirect(url_for('check4'))
    return render_template('check3.html', dato=llave_form, form=form)


@app.route('/check4', methods=['GET', 'POST'])
@login_required
def check4():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    llave_form = cursor.fetchone()
    cursor.execute(
        "select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    fecha_form = cursor.fetchone()
    form = check_list4()
    if form.validate_on_submit():
        valor = request.form.get('micheck')
        if valor == '10':
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Luces Interiores de indicadores y de salón'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Faros frontales'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Direccionales delanteras'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Luz de parqueo'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Luz retro'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Luz de frenado'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Direccionales posteriores'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Licuadora (baliza)'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Alarma de retroceso'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Bocina'))
            mysql.connection.commit()
            return redirect(url_for('check5'))
        else:
            check1 = Text(form.check1.data)
            check2 = Text(form.check2.data)
            check3 = Text(form.check3.data)
            check4 = Text(form.check4.data)
            check5 = Text(form.check5.data)
            check6 = Text(form.check6.data)
            check7 = Text(form.check7.data)
            check8 = Text(form.check8.data)
            check9 = Text(form.check9.data)
            check10 = Text(form.check10.data)
            checkobs = Text(form.checkobs.data)
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check1, 'Luces Interiores de indicadores y de salón', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check2, 'Faros frontales', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check3, 'Direccionales delanteras', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check4, 'Luz de parqueo', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check5, 'Luz retro', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check6, 'Luz de frenado', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check7, 'Direccionales posteriores', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check8, 'Licuadora (baliza)', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check9, 'Alarma de retroceso', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check10, 'Bocina', checkobs))
            mysql.connection.commit()
            return redirect(url_for('check5'))
    return render_template('check4.html', dato=llave_form, form=form)


@app.route('/check5', methods=['GET', 'POST'])
@login_required
def check5():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    llave_form = cursor.fetchone()
    cursor.execute(
        "select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    fecha_form = cursor.fetchone()
    form = check_list5()
    if form.validate_on_submit():
        valor = request.form.get('micheck')
        if valor == '2':
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Fijaciones'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Características adecuadas'))
            mysql.connection.commit()
            return redirect(url_for('check6'))
        else:
            check1 = Text(form.check1.data)
            check2 = Text(form.check2.data)
            checkobs = Text(form.checkobs.data)
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check1, 'Fijaciones', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check2, 'Características adecuadas', checkobs))
            mysql.connection.commit()
            return redirect(url_for('check6'))
    return render_template('check5.html', dato=llave_form, form=form)


@app.route('/check6', methods=['GET', 'POST'])
@login_required
def check6():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    llave_form = cursor.fetchone()
    cursor.execute(
        "select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    fecha_form = cursor.fetchone()
    form = check_list6()
    if form.validate_on_submit():
        valor = request.form.get('micheck')
        if valor == '11':
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Indicador de longitud de boom'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Indicador de ángulo (mecánico)'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Indicador de ángulo (digital)'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Indicador de radio (digital)'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Antichoque de bloques winche prin.'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Antichoque de bloques winche Aux.'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Indicador de Carga, Capacidad, Limitador'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Limitador de elevación de pluma celosía'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Indicador de rotación del tambor'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Indicador de nivelación en cabina'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Indicador velocidad de viento'))
            mysql.connection.commit()
            return redirect(url_for('check7'))
        else:
            check1 = Text(form.check1.data)
            check2 = Text(form.check2.data)
            check3 = Text(form.check3.data)
            check4 = Text(form.check4.data)
            check5 = Text(form.check5.data)
            check6 = Text(form.check6.data)
            check7 = Text(form.check7.data)
            check8 = Text(form.check8.data)
            check9 = Text(form.check9.data)
            check10 = Text(form.check10.data)
            check11 = Text(form.check10.data)
            checkobs = Text(form.checkobs.data)
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check1, 'Indicador de longitud de boom', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check2, 'Indicador de ángulo (mecánico)', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check3, 'Indicador de ángulo (digital)', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check4, 'Indicador de radio (digital)', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check5, 'Antichoque de bloques winche prin.', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check6, 'Antichoque de bloques winche Aux.', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check7, 'Indicador de Carga, Capacidad, Limitador', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check8, 'Limitador de elevación de pluma celosía', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check9, 'Indicador de rotación del tambor', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check10, 'Indicador de nivelación en cabina', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check11, 'Indicador velocidad de viento', checkobs))
            mysql.connection.commit()
            return redirect(url_for('check7'))
    return render_template('check6.html', dato=llave_form, form=form)


@app.route('/check7', methods=['GET', 'POST'])
@login_required
def check7():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    llave_form = cursor.fetchone()
    cursor.execute(
        "select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    fecha_form = cursor.fetchone()
    form = check_list7()
    if form.validate_on_submit():
        valor = request.form.get('micheck')
        if valor == '4':
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Extintor ABC'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Conos'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Adhesivos, señaléticas  de seguridad'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Superficie antideslizante'))
            mysql.connection.commit()
            return redirect(url_for('check8'))
        else:
            check1 = Text(form.check1.data)
            check2 = Text(form.check2.data)
            check3 = Text(form.check3.data)
            check4 = Text(form.check4.data)
            checkobs = Text(form.checkobs.data)
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check1, 'Extintor ABC', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check2, 'Conos', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check3, 'Adhesivos, señaléticas  de seguridad', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check4, 'Superficie antideslizante', checkobs))
            mysql.connection.commit()
            return redirect(url_for('check8'))
    return render_template('check7.html', dato=llave_form, form=form)


@app.route('/check8', methods=['GET', 'POST'])
@login_required
def check8():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    llave_form = cursor.fetchone()
    cursor.execute(
        "select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    fecha_form = cursor.fetchone()
    form = check_list8()
    if form.validate_on_submit():
        valor = request.form.get('micheck')
        if valor == '4':
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Estado del Chasis (bastidor)'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Estructura'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Soldaduras'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Vigas de estabilizadores'))
            mysql.connection.commit()
            return redirect(url_for('check9'))
        else:
            check1 = Text(form.check1.data)
            check2 = Text(form.check2.data)
            check3 = Text(form.check3.data)
            check4 = Text(form.check4.data)
            checkobs = Text(form.checkobs.data)
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check1, 'Estado del Chasis (bastidor)', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check2, 'Estructura', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check3, 'Soldaduras', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check4, 'Vigas de estabilizadores', checkobs))
            mysql.connection.commit()
            return redirect(url_for('check9'))
    return render_template('check8.html', dato=llave_form, form=form)


@app.route('/check9', methods=['GET', 'POST'])
@login_required
def check9():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    llave_form = cursor.fetchone()
    cursor.execute(
        "select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    fecha_form = cursor.fetchone()
    form = check_list9()
    if form.validate_on_submit():
        valor = request.form.get('micheck')
        if valor == '6':
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Condición de tramos'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Bases'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Soldadura'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Alineación'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Condición de Poleas'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Condición de Pasadores'))
            mysql.connection.commit()
            return redirect(url_for('check10'))
        else:
            check1 = Text(form.check1.data)
            check2 = Text(form.check2.data)
            check3 = Text(form.check3.data)
            check4 = Text(form.check4.data)
            check5 = Text(form.check5.data)
            check6 = Text(form.check6.data)
            checkobs = Text(form.checkobs.data)
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check1, 'Condición de tramos', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check2, 'Bases', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check3, 'Soldadura', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check4, 'Alineación', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check5, 'Condición de Poleas', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check6, 'Condición de Pasadores', checkobs))
            mysql.connection.commit()
            return redirect(url_for('check10'))
    return render_template('check9.html', dato=llave_form, form=form)


@app.route('/check10', methods=['GET', 'POST'])
@login_required
def check10():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    llave_form = cursor.fetchone()
    cursor.execute(
        "select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    fecha_form = cursor.fetchone()
    form = check_list10()
    if form.validate_on_submit():
        valor = request.form.get('micheck')
        if valor == '6':
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Condición de plumín'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Bases'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Soldadura'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Alineación'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Condición de Poleas'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Condición de Pasadores'))
            mysql.connection.commit()
            return redirect(url_for('check11'))
        else:
            check1 = Text(form.check1.data)
            check2 = Text(form.check2.data)
            check3 = Text(form.check3.data)
            check4 = Text(form.check4.data)
            check5 = Text(form.check5.data)
            check6 = Text(form.check6.data)
            checkobs = Text(form.checkobs.data)
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check1, 'Condición de plumín', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check2, 'Bases', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check3, 'Soldadura', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check4, 'Alineación', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check5, 'Condición de Poleas', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check6, 'Condición de Pasadores', checkobs))
            mysql.connection.commit()
            return redirect(url_for('check11'))
    return render_template('check10.html', dato=llave_form, form=form)


@app.route('/check11', methods=['GET', 'POST'])
@login_required
def check11():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    llave_form = cursor.fetchone()
    cursor.execute(
        "select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    fecha_form = cursor.fetchone()
    form = check_list11()
    if form.validate_on_submit():
        valor = request.form.get('micheck')
        if valor == '7':
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Cilindro(S) elevador de pluma'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Cilindro(S) estabilizadores'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Cilindro extensión pluma'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Cilindro(S) vigas de estabilizadores'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Circuito Hidráulico'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Winches'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Frenos'))
            mysql.connection.commit()
            return redirect(url_for('check12'))
        else:
            check1 = Text(form.check1.data)
            check2 = Text(form.check2.data)
            check3 = Text(form.check3.data)
            check4 = Text(form.check4.data)
            check5 = Text(form.check5.data)
            check6 = Text(form.check6.data)
            check7 = Text(form.check7.data)
            checkobs = Text(form.checkobs.data)
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check1, 'Cilindro(S) elevador de pluma', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check2, 'Cilindro(S) estabilizadores', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check3, 'Cilindro extensión pluma', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check4, 'Cilindro(S) vigas de estabilizadores', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check5, 'Circuito Hidráulico', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check6, 'Winches', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check7, 'Frenos', checkobs))
            mysql.connection.commit()
            return redirect(url_for('check12'))
    return render_template('check11.html', dato=llave_form, form=form)


@app.route('/check12', methods=['GET', 'POST'])
@login_required
def check12():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    llave_form = cursor.fetchone()
    cursor.execute(
        "select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    fecha_form = cursor.fetchone()
    form = check_list12()
    if form.validate_on_submit():
        valor = request.form.get('micheck')
        if valor == '3':
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Compresor'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Líneas de conducción'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Acoples'))
            mysql.connection.commit()
            return redirect(url_for('check13'))
        else:
            check1 = Text(form.check1.data)
            check2 = Text(form.check2.data)
            check3 = Text(form.check3.data)
            checkobs = Text(form.checkobs.data)
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check1, 'Compresor', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check2, 'Líneas de conducción', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check3, 'Acoples', checkobs))
            mysql.connection.commit()
            return redirect(url_for('check13'))
    return render_template('check12.html', dato=llave_form, form=form)


@app.route('/check13', methods=['GET', 'POST'])
@login_required
def check13():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    llave_form = cursor.fetchone()
    cursor.execute(
        "select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    fecha_form = cursor.fetchone()
    form = check_list13()
    if form.validate_on_submit():
        valor = request.form.get('micheck')
        if valor == '4':
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Cilindro(S) Estado de baterías'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Cilindro(S)Protección sobre carga eléctrica(fusibles)'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Interruptor Master'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Aislamiento de alambres y conectores'))
            mysql.connection.commit()
            return redirect(url_for('check14'))
        else:
            check1 = Text(form.check1.data)
            check2 = Text(form.check2.data)
            check3 = Text(form.check3.data)
            check4 = Text(form.check4.data)
            checkobs = Text(form.checkobs.data)
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check1, 'Cilindro(S) Estado de baterías', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check2, 'Cilindro(S)Protección sobre carga eléctrica(fusibles)', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check3, 'Interruptor Master', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check4, 'Aislamiento de alambres y conectores', checkobs))
            mysql.connection.commit()
            return redirect(url_for('check14'))
    return render_template('check13.html', dato=llave_form, form=form)


@app.route('/check14', methods=['GET', 'POST'])
@login_required
def check14():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    llave_form = cursor.fetchone()
    cursor.execute(
        "select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    fecha_form = cursor.fetchone()
    form = check_list14()
    if form.validate_on_submit():
        valor = request.form.get('micheck')
        if valor == '4':
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Mandos libres de atrapamientos'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Dirección del movimiento de mando'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Posición neutra de los mandos'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Señaléticas de funciones'))
            mysql.connection.commit()
            return redirect(url_for('check15'))
        else:
            check1 = Text(form.check1.data)
            check2 = Text(form.check2.data)
            check3 = Text(form.check3.data)
            check4 = Text(form.check4.data)
            checkobs = Text(form.checkobs.data)
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check1, 'Mandos libres de atrapamientos', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check2, 'Dirección del movimiento de mando', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check3, 'Posición neutra de los mandos', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check4, 'Señaléticas de funciones', checkobs))
            mysql.connection.commit()
            return redirect(url_for('check15'))
    return render_template('check14.html', dato=llave_form, form=form)


@app.route('/check15', methods=['GET', 'POST'])
@login_required
def check15():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    llave_form = cursor.fetchone()
    cursor.execute(
        "select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    fecha_form = cursor.fetchone()
    form = check_list15()
    if form.validate_on_submit():
        valor = request.form.get('micheck')
        if valor == '5':
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Cables estado estructural'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Lubricación'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Enrollado en el tambor'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Guarnido, del cable (trenzado)'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Terminal / socket / instalación'))
            mysql.connection.commit()
            return redirect(url_for('check16'))
        else:
            check1 = Text(form.check1.data)
            check2 = Text(form.check2.data)
            check3 = Text(form.check3.data)
            check4 = Text(form.check4.data)
            check5 = Text(form.check5.data)
            checkobs = Text(form.checkobs.data)
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check1, 'Cables estado estructural', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check2, 'Lubricación', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check3, 'Enrollado en el tambor', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check4, 'Guarnido, del cable (trenzado)', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check5, 'Terminal / socket / instalación', checkobs))
            mysql.connection.commit()
            return redirect(url_for('check16'))
    return render_template('check15.html', dato=llave_form, form=form)


@app.route('/check16', methods=['GET', 'POST'])
@login_required
def check16():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    llave_form = cursor.fetchone()
    cursor.execute(
        "select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    fecha_form = cursor.fetchone()
    form = check_list16()
    if form.validate_on_submit():
        valor = request.form.get('micheck')
        if valor == '4':
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Ranuras'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Radio'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Bordes'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Holguras entre poleas y ejes'))
            mysql.connection.commit()
            return redirect(url_for('check17'))
        else:
            check1 = Text(form.check1.data)
            check2 = Text(form.check2.data)
            check3 = Text(form.check3.data)
            check4 = Text(form.check4.data)
            checkobs = Text(form.checkobs.data)
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check1, 'Ranuras', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check2, 'Radio', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check3, 'Bordes', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check4, 'Holguras entre poleas y ejes', checkobs))
            mysql.connection.commit()
            return redirect(url_for('check17'))
    return render_template('check16.html', dato=llave_form, form=form)


@app.route('/check17', methods=['GET', 'POST'])
@login_required
def check17():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    llave_form = cursor.fetchone()
    cursor.execute(
        "select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    fecha_form = cursor.fetchone()
    form = check_list17()
    if form.validate_on_submit():
        valor = request.form.get('micheck')
        if valor == '8':
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Marca de capacidad'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Marca de peso'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Giro del gancho'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', '5% Abertura de garganta'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Desviación de la punta'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', '10% Desgaste del gancho'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Seguro del gancho'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Estado del gancho'))
            mysql.connection.commit()
            return redirect(url_for('check18'))
        else:
            check1 = Text(form.check1.data)
            check2 = Text(form.check2.data)
            check3 = Text(form.check3.data)
            check4 = Text(form.check4.data)
            check5 = Text(form.check5.data)
            check6 = Text(form.check6.data)
            check7 = Text(form.check7.data)
            check8 = Text(form.check8.data)
            checkobs = Text(form.checkobs.data)
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check1, 'Marca de capacidad', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check2, 'Marca de peso', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check3, 'Giro del gancho', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check4, '5% Abertura de garganta', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check5, 'Desviación de la punta', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check6, '10% Desgaste del gancho', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check7, 'Seguro del gancho', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check8, 'Estado del gancho', checkobs))
            mysql.connection.commit()
            return redirect(url_for('check18'))
    return render_template('check17.html', dato=llave_form, form=form)


@app.route('/check18', methods=['GET', 'POST'])
@login_required
def check18():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    llave_form = cursor.fetchone()
    cursor.execute(
        "select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    fecha_form = cursor.fetchone()
    form = check_list18()
    if form.validate_on_submit():
        valor = request.form.get('micheck')
        if valor == '8':
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Marca de capacidad aux'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Marca de peso aux'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Giro del gancho aux'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', '5% Abertura de garganta aux'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Desviación de la punta aux'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', '10% Desgaste del gancho aux'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Seguro del gancho aux'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Estado del gancho aux'))
            mysql.connection.commit()
            return redirect(url_for('check19'))
        else:
            check1 = Text(form.check1.data)
            check2 = Text(form.check2.data)
            check3 = Text(form.check3.data)
            check4 = Text(form.check4.data)
            check5 = Text(form.check5.data)
            check6 = Text(form.check6.data)
            check7 = Text(form.check7.data)
            check8 = Text(form.check8.data)
            checkobs = Text(form.checkobs.data)
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check1, 'Marca de capacidad aux', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check2, 'Marca de peso aux', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check3, 'Giro del gancho aux', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check4, '5% Abertura de garganta aux', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check5, 'Desviación de la punta aux', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check6, '10% Desgaste del gancho aux', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check7, 'Seguro del gancho aux', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check8, 'Estado del gancho aux', checkobs))
            mysql.connection.commit()
            return redirect(url_for('check19'))
    return render_template('check18.html', dato=llave_form, form=form)


@app.route('/check19', methods=['GET', 'POST'])
@login_required
def check19():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    llave_form = cursor.fetchone()
    cursor.execute(
        "select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    fecha_form = cursor.fetchone()
    form = check_list19()
    if form.validate_on_submit():
        valor = request.form.get('micheck')
        if valor == '9':
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Accesos y puntos de apoyo'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Puerta seguro posic. abierto y posic. cerrado'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Vidrios, parabrisas y techo'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Limpia parabrisas'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Asiento'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Cinturón de seguridad'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Espejos laterales de cabina'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Fijación de volante'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Condición de la cabina/estructura'))
            mysql.connection.commit()
            return redirect(url_for('check20'))
        else:
            check1 = Text(form.check1.data)
            check2 = Text(form.check2.data)
            check3 = Text(form.check3.data)
            check4 = Text(form.check4.data)
            check5 = Text(form.check5.data)
            check6 = Text(form.check6.data)
            check7 = Text(form.check7.data)
            check8 = Text(form.check8.data)
            check9 = Text(form.check9.data)
            checkobs = Text(form.checkobs.data)
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check1, 'Accesos y puntos de apoyo', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check2, 'Puerta seguro posic. abierto y posic. cerrado', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check3, 'Vidrios, parabrisas y techo', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check4, 'Limpia parabrisas', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check5, 'Asiento', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check6, 'Cinturón de seguridad', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check7, 'Espejos laterales de cabina', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check8, 'Fijación de volante', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check9, 'Condición de la cabina/estructura', checkobs))
            mysql.connection.commit()
            return redirect(url_for('check20'))
    return render_template('check19.html', dato=llave_form, form=form)


@app.route('/check20', methods=['GET', 'POST'])
@login_required
def check20():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    llave_form = cursor.fetchone()
    cursor.execute(
        "select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    fecha_form = cursor.fetchone()
    form = check_list20()
    if form.validate_on_submit():
        valor = request.form.get('micheck')
        if valor == '7':
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Estado del Chasis, soldadura'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Escape (guarda)'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Escaleras, manijas, guardas'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Suspensión, transmisión, dirección'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Fijación Pernos, espárragos, tuercas'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Alarma de retroceso'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Bocina'))
            mysql.connection.commit()
            return redirect(url_for('check21'))
        else:
            check1 = Text(form.check1.data)
            check2 = Text(form.check2.data)
            check3 = Text(form.check3.data)
            check4 = Text(form.check4.data)
            check5 = Text(form.check5.data)
            check6 = Text(form.check6.data)
            check7 = Text(form.check7.data)
            checkobs = Text(form.checkobs.data)
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check1, 'Estado del Chasis, soldadura', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check2, 'Escape (guarda)', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check3, 'Escaleras, manijas, guardas', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check4, 'Suspensión, transmisión, dirección', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check5, 'Fijación Pernos, espárragos, tuercas', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check6, 'Alarma de retroceso', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check7, 'Bocina', checkobs))
            mysql.connection.commit()
            return redirect(url_for('check21'))
    return render_template('check20.html', dato=llave_form, form=form)


@app.route('/check21', methods=['GET', 'POST'])
@login_required
def check21():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    llave_form = cursor.fetchone()
    cursor.execute(
        "select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    fecha_form = cursor.fetchone()
    form = check_list21()
    if form.validate_on_submit():
        valor = request.form.get('micheck')
        if valor == '7':
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Neumáticos, apropiados según el fabricante'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Bandas de rodadura (neumáticos)'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Estructura (neumáticos)'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Tren de rodaje'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Zapatas (tren de rodaje)'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Rodillos (tren de rodaje)'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Catalinas (tren de rodaje)'))
            mysql.connection.commit()
            return redirect(url_for('check22'))
        else:
            check1 = Text(form.check1.data)
            check2 = Text(form.check2.data)
            check3 = Text(form.check3.data)
            check4 = Text(form.check4.data)
            check5 = Text(form.check5.data)
            check6 = Text(form.check6.data)
            check7 = Text(form.check7.data)
            checkobs = Text(form.checkobs.data)
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check1, 'Neumáticos, apropiados según el fabricante', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check2, 'Bandas de rodadura (neumáticos)', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check3, 'Estructura (neumáticos)', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check4, 'Tren de rodaje', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check5, 'Zapatas (tren de rodaje)', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check6, 'Rodillos (tren de rodaje)', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check7, 'Catalinas (tren de rodaje)', checkobs))
            mysql.connection.commit()
            return redirect(url_for('check22'))
    return render_template('check21.html', dato=llave_form, form=form)


@app.route('/check22', methods=['GET', 'POST'])
@login_required
def check22():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    llave_form = cursor.fetchone()
    cursor.execute(
        "select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    fecha_form = cursor.fetchone()
    form = check_list22()
    if form.validate_on_submit():
        valor = request.form.get('micheck')
        if valor == '2':
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Gases de escape entubados'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Fugas de aceite por cuerpo del motor'))
            mysql.connection.commit()
            return redirect(url_for('check23'))
        else:
            check1 = Text(form.check1.data)
            check2 = Text(form.check2.data)
            checkobs = Text(form.checkobs.data)
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check1, 'Gases de escape entubados', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check2, 'Fugas de aceite por cuerpo del motor', checkobs))
            mysql.connection.commit()
            return redirect(url_for('check23'))
    return render_template('check22.html', dato=llave_form, form=form)


@app.route('/check23', methods=['GET', 'POST'])
@login_required
def check23():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    llave_form = cursor.fetchone()
    cursor.execute(
        "select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    fecha_form = cursor.fetchone()
    form = check_list23()
    if form.validate_on_submit():
        valor = request.form.get('micheck')
        if valor == '3':
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Tapa del combustible'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Conductos'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Deposito de combustible'))
            mysql.connection.commit()
            return redirect(url_for('check24'))
        else:
            check1 = Text(form.check1.data)
            check2 = Text(form.check2.data)
            check3 = Text(form.check3.data)
            checkobs = Text(form.checkobs.data)
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check1, 'Tapa del combustible', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check2, 'Conductos', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check3, 'Deposito de combustible', checkobs))
            mysql.connection.commit()
            return redirect(url_for('check24'))

    return render_template('check23.html', dato=llave_form, form=form)


@app.route('/check24', methods=['GET', 'POST'])
@login_required
def check24():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    llave_form = cursor.fetchone()
    cursor.execute(
        "select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    fecha_form = cursor.fetchone()
    form = check_list24()
    if form.validate_on_submit():
        valor = request.form.get('micheck')
        if valor == '3':
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Pernos / tuercas'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Piñón, cremallera, dientes, guardas'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Pin / Seguro de tornamesa'))
            mysql.connection.commit()
            return redirect(url_for('check25'))
        else:
            check1 = Text(form.check1.data)
            check2 = Text(form.check2.data)
            check3 = Text(form.check3.data)
            checkobs = Text(form.checkobs.data)
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check1, 'Pernos / tuercas', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check2, 'Piñón, cremallera, dientes, guardas', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check3, 'Pin / Seguro de tornamesa', checkobs))
            mysql.connection.commit()
            return redirect(url_for('check25'))

    return render_template('check24.html', dato=llave_form, form=form)


@app.route('/check25', methods=['GET', 'POST'])
@login_required
def check25():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    llave_form = cursor.fetchone()
    cursor.execute(
        "select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    fecha_form = cursor.fetchone()
    form = check_list25()
    if form.validate_on_submit():
        valor = request.form.get('micheck')
        if valor == '5':
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Mecanismos para levantar y bajar cargas'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Mecanismos para levantar y bajar pluma'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Mecanismo para extender y retraer pluma'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Mecanismo de giro'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                        (llave_form, fecha_form, 'S', 'Mecanismo de viaje y/o recorrido'))
            mysql.connection.commit()
            return redirect(url_for('CHECK_FINAL'))
        else:
            check1 = Text(form.check1.data)
            check2 = Text(form.check2.data)
            check3 = Text(form.check3.data)
            check4 = Text(form.check4.data)
            check5 = Text(form.check5.data)
            checkobs = Text(form.checkobs.data)
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check1, 'Mecanismos para levantar y bajar cargas', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check2, 'Mecanismos para levantar y bajar pluma', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check3, 'Mecanismo para extender y retraer pluma', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check4, 'Mecanismo de giro', checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',
                        (llave_form, fecha_form, check5, 'Mecanismo de viaje y/o recorrido', checkobs))
            mysql.connection.commit()
            return redirect(url_for('CHECK_FINAL'))

    return render_template('check25.html', dato=llave_form, form=form)


@app.route('/CHECK_FINAL', methods=['GET', 'POST'])
@login_required
def CHECK_FINAL():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    llave_form = cursor.fetchone()
    cursor.execute(
        "select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    fecha_form = cursor.fetchone()
    form = CHECK_LIST_FIN()
    if form.validate_on_submit():
        check7 = Text(form.check7.data)
        cur = mysql.connection.cursor()
        cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                    (llave_form, fecha_form, check7, 'ZONA INSPECCIONADA'))
        cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                    (llave_form, fecha_form, check7, 'ENSAYO APLICADO'))
        cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',
                    (llave_form, fecha_form, check7, 'REFERENCIA'))
        mysql.connection.commit()
        return redirect(url_for('PRUE_CARG'))

    return render_template('CHECK_FINAL.html', dato=llave_form, form=form)


@app.route('/REP_LMI', methods=['GET', 'POST'])
@login_required
def REP_LMI():
    form = datos_reporte()
    if form.validate_on_submit():
        return f"email ={request.form['email']} | clave ={request.form['password']}"
    return render_template('REP_LMI.html', form=form)


@app.route('/PRUE_CARG', methods=['GET', 'POST'])
@login_required
def PRUE_CARG():
    form = prueba_carga()
    print(form.errors)
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    llave_form = cursor.fetchone()
    if form.validate_on_submit():
        p1 = form.carga_utli_est.data
        p2 = form.peso_carga_est.data
        p3 = form.peso_aparejo_est.data
        valor_t = p1+p2+p3
        l_plu = form.long_pluma_est.data
        r_oper = form.rad_oper_est.data
        ang_plu = form.ang_pluma_est.data
        cap_max = form.cap_maxima_est.data
        v_total = l_plu+r_oper+ang_plu+cap_max
        carga = form.carga.data
        est1 = form.ESTAB1.data
        est2 = form.ESTAB2.data
        est3 = form.ESTAB3.data
        est4 = form.ESTAB4.data
        carga2 = form.carga2.data
        est12 = form.ESTAB12.data
        est22 = form.ESTAB22.data
        est32 = form.ESTAB32.data
        est42 = form.ESTAB42.data
        carga3 = form.carga3.data
        est13 = form.ESTAB13.data
        est23 = form.ESTAB23.data
        est33 = form.ESTAB33.data
        est43 = form.ESTAB43.data
        cursor.execute('insert into prue_carg_est (id_formulario,carga_utilizada,peso_carga,peso_aparejos,peso_total,medida,long_pluma,radio_ope,ang_pluma,cap_max,tiempo,carga,estab_1,estab_2,estab_3,estab_4) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                       (llave_form, p1, p2, p3, valor_t, 'Kg', l_plu, r_oper, ang_plu, cap_max, '5', carga, est1, est2, est3, est4))
        cursor.execute('insert into prue_carg_est (id_formulario,carga_utilizada,peso_carga,peso_aparejos,peso_total,medida,long_pluma,radio_ope,ang_pluma,cap_max,tiempo,carga,estab_1,estab_2,estab_3,estab_4) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                       (llave_form, p1, p2, p3, valor_t, 'Kg', l_plu, r_oper, ang_plu, cap_max, '5', carga2, est12, est22, est32, est42))
        cursor.execute('insert into prue_carg_est (id_formulario,carga_utilizada,peso_carga,peso_aparejos,peso_total,medida,long_pluma,radio_ope,ang_pluma,cap_max,tiempo,carga,estab_1,estab_2,estab_3,estab_4) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                       (llave_form, p1, p2, p3, valor_t, 'Kg', l_plu, r_oper, ang_plu, cap_max, '5', carga3, est13, est23, est33, est43))
        mysql.connection.commit()
        return redirect('PRUE_CARG_3')
    return render_template('PRUE_CARG.html', form=form)


@app.route('/PRUE_CARG_3', methods=['GET', 'POST'])
@login_required
def PRUE_CARG3():
    form = prueba_carga3()
    print(form.errors)
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    llave_form = cursor.fetchone()
    if form.validate_on_submit():
        p1 = form.carga_utli_din.data
        p2 = form.peso_carga_din.data
        p3 = form.peso_aparejo_din.data
        valor_t = p1+p2+p3
        p5 = form.long_pluma_din.data
        p6 = form.rad_oper_din.data
        p7 = form.ang_pluma_din.data
        p8 = form.cap_maxima_din.data
        v_total = p5+p6+p7+p8
        tor = form.check1_pru_car.data
        tor1 = form.check2_pru_car.data
        tor2 = form.check3_pru_car.data
        tor3 = form.check4_pru_car.data
        cursor.execute('insert into prue_carg_din (id_formulario,carga_utilizada,peso_carga,peso_aparejos,medida,peso_total,long_pluma,radio_ope,ang_pluma,cap_max,tornamesa,sis_mov_fre,est_estabilizado,cond_estab_maq) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                       (llave_form, p1, p2, p3, 'Kg', valor_t, p5, p6, p7, p8, tor, tor1, tor2, tor3))
        mysql.connection.commit()
        return redirect('REP_FOTO_CARGA')
    return render_template('PRUE_CARG_3.html', form=form)


@app.route('/REP_FOTO_CARGA', methods=['GET', 'POST'])
@login_required
def REP_FOTO_CARGA():
    form = UploadForm()  # carga request.from y request.file
    if form.validate_on_submit():
        f = form.photo.data
        filename = secure_filename(f.filename)
        f.save(app.root_path+"/static/img/subidas/"+filename)
        return redirect(url_for('inicio_foto'))
    return render_template('REP_FOTO_CARGA.html', form=form)


@app.route('/REP_FOTO', methods=['GET', 'POST'])
@login_required
def REP_FOTO():
    form = UploadForm()  # carga request.from y request.file
    if form.validate_on_submit():
        f = form.photo.data
        filename = secure_filename(f.filename)
        f.save(app.root_path+"/static/img/subidas/"+filename)
        return redirect(url_for('reporte_foto'))
    return render_template('REP_FOTO.html', form=form)


@app.route('/RESULTADOS', methods=['GET', 'POST'])
@login_required
def RESULTADOS():
    # if request.method=="POST":
    cursor = mysql.connection.cursor()
    cursor.execute("select MAX(id_formulario) from formulario")
    id_f = cursor.fetchone()
    cursor.execute("select codigo from equipos_ins where nombre = 'MULTIMETRO' and nombre_insp = (select nom_inspe_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario));")
    cod_int = cursor.fetchone()
    cursor.execute("select fecha_calib from equipos_ins where nombre = 'MULTIMETRO' and nombre_insp = (select nom_inspe_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario));")
    fec_cal = cursor.fetchone()
    cursor.execute("select codigo from equipos_ins where nombre = 'CINTA METRICA' and nombre_insp = (select nom_inspe_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario));")
    cod_int1 = cursor.fetchone()
    cursor.execute("select fecha_calib from equipos_ins where nombre = 'CINTA METRICA' and nombre_insp = (select nom_inspe_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario));")
    fec_cal1 = cursor.fetchone()
    cursor.execute("select codigo from equipos_ins where nombre = 'PIE DE REY' and nombre_insp = (select nom_inspe_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario));")
    cod_int2 = cursor.fetchone()
    cursor.execute("select fecha_calib from equipos_ins where nombre = 'PIE DE REY' and nombre_insp = (select nom_inspe_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario));")
    fec_cal2 = cursor.fetchone()
    cursor.execute("select codigo from equipos_ins where nombre = 'FLEXOMETRO' and nombre_insp = (select nom_inspe_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario));")
    cod_int3 = cursor.fetchone()
    cursor.execute("select fecha_calib from equipos_ins where nombre = 'FLEXOMETRO' and nombre_insp = (select nom_inspe_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario));")
    fec_cal3 = cursor.fetchone()
    cursor.execute("select codigo from equipos_ins where nombre = 'GONIOMETRO' and nombre_insp = (select nom_inspe_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario));")
    cod_int4 = cursor.fetchone()
    cursor.execute("select fecha_calib from equipos_ins where nombre = 'GONIOMETRO' and nombre_insp = (select nom_inspe_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario));")
    fec_cal4 = cursor.fetchone()
    cursor.execute("select count(1) from check_list where valor ='S' and id_formulario = (select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario));")
    count_S = cursor.fetchone()
    number_of_rows_S = count_S[0]
    cursor.execute("select count(1) from check_list where valor ='DL' and id_formulario = (select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario));")
    count_DL = cursor.fetchone()
    number_of_rows_DL = count_DL[0]
    cursor.execute("select count(1) from check_list where valor ='DG' and id_formulario = (select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario));")
    count_DG = cursor.fetchone()
    number_of_rows_DG = count_DG[0]
    cursor.execute('insert into resultados (cod_ins,nom_ins,fecha_calib,id_formulario,DL_res,DG_res,S_res,conforme) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',
                   (cod_int, 'MULTIMETRO', fec_cal, id_f, number_of_rows_DL, number_of_rows_DG, number_of_rows_S, 1))
    cursor.execute('insert into resultados (cod_ins,nom_ins,fecha_calib,id_formulario,DL_res,DG_res,S_res,conforme) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',
                   (cod_int1, 'CINTA METRICA', fec_cal1, id_f, number_of_rows_DL, number_of_rows_DG, number_of_rows_S, 1))
    cursor.execute('insert into resultados (cod_ins,nom_ins,fecha_calib,id_formulario,DL_res,DG_res,S_res,conforme) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',
                   (cod_int2, 'PIE DE REY', fec_cal2, id_f, number_of_rows_DL, number_of_rows_DG, number_of_rows_S, 1))
    cursor.execute('insert into resultados (cod_ins,nom_ins,fecha_calib,id_formulario,DL_res,DG_res,S_res,conforme) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',
                   (cod_int3, 'FLEXOMETRO', fec_cal3, id_f, number_of_rows_DL, number_of_rows_DG, number_of_rows_S, 1))
    cursor.execute('insert into resultados (cod_ins,nom_ins,fecha_calib,id_formulario,DL_res,DG_res,S_res,conforme) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',
                   (cod_int4, 'GONIOMETRO', fec_cal4, id_f, number_of_rows_DL, number_of_rows_DG, number_of_rows_S, 1))
    mysql.connection.commit()
    if number_of_rows_DG >= 1:
        cond = 'EQUIPO NO CONFORME'
        return render_template('RESULTADOS.html', a=cod_int, fec1=fec_cal, b=cod_int1, fec2=fec_cal1,
                               c=cod_int2, fec3=fec_cal2, d=cod_int3, fec4=fec_cal3, e=cod_int4,
                               fec5=fec_cal4, S=count_S, DL=count_DL, DG=count_DG, C=cond, id_f=id_f)
    if number_of_rows_DL >= 0 and number_of_rows_DG == 0:
        cond = 'EQUIPO CONFORME CON DEFECTOS LEVES'
        return render_template('RESULTADOS.html', a=cod_int, fec1=fec_cal, b=cod_int1, fec2=fec_cal1,
                               c=cod_int2, fec3=fec_cal2, d=cod_int3, fec4=fec_cal3, e=cod_int4,
                               fec5=fec_cal4, S=count_S, DL=count_DL, DG=count_DG, C=cond, id_f=id_f)
    cond = 'EQUIPO CONFORME'
    return render_template('RESULTADOS.html', a=cod_int, fec1=fec_cal, b=cod_int1, fec2=fec_cal1,
                           c=cod_int2, fec3=fec_cal2, d=cod_int3, fec4=fec_cal3, e=cod_int4, fec5=fec_cal4,
                           S=count_S, DL=count_DL, DG=count_DG, C=cond, id_f=id_f)


@app.route('/genera_pdf')
@login_required
def genera_pdf():
    env = Environment(loader=FileSystemLoader('templates'))
    options = {
        'page-size': 'Letter',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'no-outline': None
    }
    pdfkit.from_file('resumen.html', 'out.pdf', options=options)
    return 'OK'


@app.route('/CERTIFICADO_GM', methods=['GET', 'POST'])
@login_required
def CERTIFICADO_GM():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select llave_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    nom_form = cursor.fetchone()
    cursor.execute(
        "select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_insp = cursor.fetchone()
    cursor.execute(
        "select fecha_emision_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_emi = cursor.fetchone()
    cursor.execute(
        "select fecha_expiracion_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_exp = cursor.fetchone()
    cursor.execute(
        "select lugar_ins_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    lugar = cursor.fetchone()
    cursor.execute(
        "select nom_inspe_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    inpe = cursor.fetchone()
    cursor.execute(
        "select codint_datos_equipo from datos_equipo where id_formulario = (select MAX(id_formulario) from formulario);")
    cod_inter = cursor.fetchone()
    cursor.execute(
        "select CAP_MAX_Capacidad_Trabajo from capacidad_trabajo where id_formulario = (select MAX(id_formulario) from formulario);")
    cap_max = cursor.fetchone()
    cursor.execute(
        "select modelo_datos_equipo from datos_equipo where id_formulario = (select MAX(id_formulario) from formulario);")
    modelo = cursor.fetchone()
    cursor.execute(
        "select MARCA_datos_equipo from datos_equipo where id_formulario = (select MAX(id_formulario) from formulario);")
    marca = cursor.fetchone()
    cursor.execute(
        "select anio_datos_equipo from datos_equipo where id_formulario = (select MAX(id_formulario) from formulario);")
    ani = cursor.fetchone()
    cursor.execute(
        "select serie_datos_equipo from datos_equipo where id_formulario = (select MAX(id_formulario) from formulario);")
    serie = cursor.fetchone()
    cursor.execute(
        "select cod_ins from resultados where nom_ins = 'MULTIMETRO' and id_formulario = (select MAX(id_formulario) from formulario);")
    cod1 = cursor.fetchone()
    cursor.execute(
        "select nom_ins from resultados where nom_ins = 'MULTIMETRO' and id_formulario = (select MAX(id_formulario) from formulario);")
    nom1 = cursor.fetchone()
    cursor.execute(
        "select fecha_calib from resultados where nom_ins = 'MULTIMETRO' and id_formulario = (select MAX(id_formulario) from formulario);")
    fec_cal1 = cursor.fetchone()
    cursor.execute(
        "select cod_ins from resultados where nom_ins = 'CINTA METRICA' and id_formulario = (select MAX(id_formulario) from formulario);")
    cod2 = cursor.fetchone()
    cursor.execute(
        "select nom_ins from resultados where nom_ins = 'CINTA METRICA' and id_formulario = (select MAX(id_formulario) from formulario);")
    nom2 = cursor.fetchone()
    cursor.execute(
        "select fecha_calib from resultados where nom_ins = 'CINTA METRICA' and id_formulario = (select MAX(id_formulario) from formulario);")
    fec_cal2 = cursor.fetchone()
    cursor.execute(
        "select cod_ins from resultados where nom_ins = 'PIE DE REY' and id_formulario = (select MAX(id_formulario) from formulario);")
    cod3 = cursor.fetchone()
    cursor.execute(
        "select nom_ins from resultados where nom_ins = 'PIE DE REY' and id_formulario = (select MAX(id_formulario) from formulario);")
    nom3 = cursor.fetchone()
    cursor.execute(
        "select fecha_calib from resultados where nom_ins = 'PIE DE REY' and id_formulario = (select MAX(id_formulario) from formulario);")
    fec_cal3 = cursor.fetchone()
    cursor.execute(
        "select cod_ins from resultados where nom_ins = 'FLEXOMETRO' and id_formulario = (select MAX(id_formulario) from formulario);")
    cod4 = cursor.fetchone()
    cursor.execute(
        "select nom_ins from resultados where nom_ins = 'FLEXOMETRO' and id_formulario = (select MAX(id_formulario) from formulario);")
    nom4 = cursor.fetchone()
    cursor.execute(
        "select fecha_calib from resultados where nom_ins = 'FLEXOMETRO' and id_formulario = (select MAX(id_formulario) from formulario);")
    fec_cal4 = cursor.fetchone()
    cursor.execute(
        "select cod_ins from resultados where nom_ins = 'GONIOMETRO' and id_formulario = (select MAX(id_formulario) from formulario);")
    cod5 = cursor.fetchone()
    cursor.execute(
        "select nom_ins from resultados where nom_ins = 'GONIOMETRO' and id_formulario = (select MAX(id_formulario) from formulario);")
    nom5 = cursor.fetchone()
    cursor.execute(
        "select fecha_calib from resultados where nom_ins = 'GONIOMETRO' and id_formulario = (select MAX(id_formulario) from formulario);")
    fec_cal5 = cursor.fetchone()

    return render_template('CERTIFICADO_GM.html', datos=nom_form,
                           fec1=fec_insp, fec2=fec_emi, fec3=fec_exp, lugar=lugar, inspector=inpe,
                           cod_inter=cod_inter, cap_max=cap_max, modelo=modelo, marca=marca, ani=ani,
                           serie=serie, cod1=cod1, nom1=nom1, fec_cal1=fec_cal1, cod2=cod2, nom2=nom2,
                           fec_cal2=fec_cal2, cod3=cod3, nom3=nom3, fec_cal3=fec_cal3, cod4=cod4, nom4=nom4,
                           fec_cal4=fec_cal4, cod5=cod5, nom5=nom5, fec_cal5=fec_cal5)








@app.errorhandler(404)
def page_not_found(error):
    return render_template("error.html", error="Página no encontrada..."), 404


@app.route('/cons_404', methods=['GET', 'POST'])
def cons_404():
    return render_template('404_cons.html')


@app.route('/login', methods=['get', 'post'])
def login():
    from aplicacion.models import Usuarios
    # Control de permisos
    if current_user.is_authenticated:
        # return 'OK'
        return redirect(url_for("inicio_new"))
    form = LoginForm()
    if form.validate_on_submit():
        user = Usuarios.query.filter_by(username=form.username.data).first()
        print(user)
        pas1 = Usuarios.query.filter_by(password=form.password.data).first()
        print(pas1)
        pas = user.verify_password(form.password.data)
        print(pas)
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            next = request.args.get('next')
            return redirect(next or url_for('inicio_new'))
        form.username.errors.append("Usuario o contraseña incorrectas.")
    return render_template('login.html', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('inicio'))


@app.route('/perfil/<username>', methods=["get", "post"])
@login_required
def perfil(username):
    from aplicacion.models import Usuarios
    user = Usuarios.query.filter_by(username=username).first()
    if user is None:
        render_template("404.html")
    form = FormUsuario(request.form, obj=user)
    del form.password
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        return redirect(url_for("inicio"))
    return render_template("usuarios_new.html", form=form, perfil=True)


@login_manager.user_loader
def load_user(user_id):
    from aplicacion.models import Usuarios
    return Usuarios.query.get(int(user_id))




@app.route('/bus_form', methods = ['POST', 'GET'])
@login_required
def bus_form():
    form = list_formulario()
    if request.method == 'POST':
        nombre = request.form['nombre']
        print(nombre)
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM formulario WHERE desc_formulario = %s order by fecha_inspec_formulario desc", [nombre])
        data = cursor.fetchall()
        cursor.execute("SELECT cod_form FROM formulario WHERE desc_formulario = %s ", [nombre])
        formu = cursor.fetchone()
        cursor.execute("SELECT id_formulario FROM formulario WHERE desc_formulario = %s ", [nombre])
        num_rep = cursor.fetchone()
        print(formu)
        print(num_rep)
        if formu == ('frpol',):
            cursor.execute("select id from frpol where id_formulario = %s ",[num_rep])
            data1 = cursor.fetchone()
            print(data1)
            return render_template('listar_form.html', data=data,contact=data1[0])
        if formu == ('freca',):
            cursor.execute("select id from freca where id_formulario = %s ",[num_rep])
            data1 = cursor.fetchone()
            print(data1)
            return render_template('listar_form.html', data=data,contact=data1[0])
        if formu == ('frcad',):
            cursor.execute("select id from frcad where id_formulario = %s ",[num_rep])
            data1 = cursor.fetchone()
            print(data1)
            return render_template('listar_form.html', data=data,contact=data1[0])
        if formu == ('frefs',):
            cursor.execute("select id from frefs where id_formulario = %s ",[num_rep])
            data1 = cursor.fetchone()
            print(data1)
            return render_template('listar_form.html', data=data,contact=data1[0])
        if formu == ('frgan',):
            cursor.execute("select id from frgan where id_formulario = %s ",[num_rep])
            data1 = cursor.fetchone()
            print(data1)
            return render_template('listar_form.html', data=data,contact=data1[0])
        if formu == ('frgri',):
            cursor.execute("select id from frgri where id_formulario = %s ",[num_rep])
            data1 = cursor.fetchone()
            print(data1)
            return render_template('listar_form.html', data=data,contact=data1[0])
        if formu == ('frkpi',):
            cursor.execute("select id from frkpi where id_formulario = %s ",[num_rep])
            data1 = cursor.fetchone()
            print(data1)
            return render_template('listar_form.html', data=data,contact=data1[0])
        if formu == ('frqru',):
            cursor.execute("select id from frqru where id_formulario = %s ",[num_rep])
            data1 = cursor.fetchone()
            print(data1)
            return render_template('listar_form.html', data=data,contact=data1[0])
        if formu == ('frsep',):
            cursor.execute("select id from frsep where id_formulario = %s ",[num_rep])
            data1 = cursor.fetchone()
            print(data1)
            return render_template('listar_form.html', data=data,contact=data1[0])
        if formu == ('frhor',):
            cursor.execute("select id from frhor where id_formulario = %s ",[num_rep])
            data1 = cursor.fetchone()
            print(data1)
            return render_template('listar_form.html', data=data,contact=data1[0])
        if formu == ('frppr',):
            cursor.execute("select id from frppr where id_formulario = %s ",[num_rep])
            data1 = cursor.fetchone()
            print(data1)
            return render_template('listar_form.html', data=data,contact=data1[0])
        if formu == ('frapa',):
            cursor.execute("select id from frapa where id_formulario = %s ",[num_rep])
            data1 = cursor.fetchone()
            print(data1)
            return render_template('listar_form.html', data=data,contact=data1[0])
        if formu == ('frttr',):
            cursor.execute("select id from frttr where id_formulario = %s ",[num_rep])
            data1 = cursor.fetchone()
            print(data1)
            return render_template('listar_form.html', data=data,contact=data1[0])
    return render_template("bus_form.html", form=form) 


@app.route('/listar_form/<id>', methods=['POST', 'GET'])
@login_required
def listar_form(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM frpol  ')
    data1 = cur.fetchall()
    cur.close()
    print(data1)
    return render_template('listar_form.html')
