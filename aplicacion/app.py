from typing import Text
from flask import Flask , render_template, request, redirect, url_for, flash, make_response
from flask_sqlalchemy import SQLAlchemy
from aplicacion import config
from aplicacion.forms import datos_equipo, datos_reporte, check_list2, check_list3,FormArticulo
from aplicacion.forms import check_list4, check_list5, check_list6, check_list7, check_list8, check_list9
from aplicacion.forms import check_list10, check_list11, check_list12,check_list13, check_list14, check_list15
from aplicacion.forms import check_list16, check_list17, check_list18, check_list19, check_list20, check_list21
from aplicacion.forms import check_list22, check_list23, check_list24, check_list25, Publicaciones, CHECK_LIST_FIN
from aplicacion.forms import prueba_carga,check_list1,prueba_carga3
from aplicacion.forms import formu1,formu2
from aplicacion.forms import  LoginForm, UploadForm
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
from flask_wtf.file import FileField, FileRequired
from wtforms.fields.html5 import DateField
from jinja2 import Environment, FileSystemLoader
from os import listdir
from flask_login import LoginManager, login_user, logout_user, login_required,\
    current_user
from aplicacion.forms import LoginForm,FormUsuario
import pdfkit
import os


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

#setting
app.secret_key = 'millave'

@login_manager.user_loader
def load_user(user_id):
    return (user_id)

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
    return render_template("inicio_1.html", articulos=articulos,categorias=categorias, categoria=categoria)


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
    form= UploadForm() # carga request.from y request.file
    if form.validate_on_submit():
        f = form.photo.data
        filename = secure_filename(f.filename)
        f.save(app.root_path+"/static/img/subidas/"+filename)
        return redirect(url_for('inicio_foto'))
    return render_template('upload.html', form=form)


@app.route('/upload_1', methods=['get', 'post'])
def upload_1():
    form= UploadForm() # carga request.from y request.file
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

@app.route('/home', methods=['GET','POST'])
@login_required
def home():
    cursor = mysql.connection.cursor()
    cursor.execute("select llave_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
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
        cursor.execute("select llave_formulario from formulario where id_formulario = 1;")
        cursor.execute('insert into formulario (llave_formulario,desc_formulario,fecha_inspec_formulario,fecha_emision_formulario,fecha_expiracion_formulario,lugar_ins_formulario,nom_inspe_formulario,obs1_formulario) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',('FR-INSP-003.06','REPORTE DE INSPECCIÓN DE GRÚAS',fecha_insp,fecha_emi,fecha_exp,lugar_ins,nombre_ins,''))
        mysql.connection.commit()
        flash('Guardado Correctamente')
        datos = cursor.fetchone()
        print(datos)
        return redirect(url_for('resumen'))
    return render_template('home.html', form=form,datos=nom_form)

@app.route('/home_1', methods=['GET','POST'])
@login_required
def home_1():
    cursor = mysql.connection.cursor()
    cursor.execute("select nombre from articulos where id = 4;")
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
        cursor.execute('insert into formulario (llave_formulario,desc_formulario,fecha_inspec_formulario,fecha_emision_formulario,fecha_expiracion_formulario,lugar_ins_formulario,nom_inspe_formulario,obs1_formulario) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',(nom_form,'Reporte Inspeccion Poleas',fecha_insp,fecha_emi,fecha_exp,lugar_ins,nombre_ins,''))
        mysql.connection.commit()
        flash('Guardado Correctamente')
        datos = cursor.fetchone()
        print(datos)
        #return 'OK'
        return redirect(url_for('formu_1'))
    return render_template('home_1.html', form=form,datos=nom_form)


@app.route('/home_2', methods=['GET','POST'])
@login_required
def home_2():
    cursor = mysql.connection.cursor()
    cursor.execute("select nombre from articulos where id = 5;")
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
        cursor.execute('insert into formulario (llave_formulario,desc_formulario,fecha_inspec_formulario,fecha_emision_formulario,fecha_expiracion_formulario,lugar_ins_formulario,nom_inspe_formulario,obs1_formulario) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',(nom_form,'Reporte Inspeccion Poleas',fecha_insp,fecha_emi,fecha_exp,lugar_ins,nombre_ins,''))
        mysql.connection.commit()
        flash('Guardado Correctamente')
        datos = cursor.fetchone()
        print(datos)
        #return 'OK'
        return redirect(url_for('formu_2'))
    return render_template('home_2.html', form=form,datos=nom_form)


@app.route('/formu_1', methods=['GET','POST'])
@login_required
def formu_1():
    form = formu1()
    if form.validate_on_submit():
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
        num = request.form['num']
        ref = request.form['ref']
        cod_enii = request.form['cod_enii']
        ancho = request.form['ancho']
        diam = request.form['diam']
        vt = request.form['vt']
        pt = request.form['pt']
        cur = mysql.connection.cursor()
        cur.execute("select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
        llave_form = cur.fetchone()
        cur.execute("select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
        fecha_form = cur.fetchone()
        cur.execute('insert into form2 (id_formulario,fec_formulario,proc,revis,nivel_il,con_sup,met_insp,tipo_il,check1,check2,check3,detalle,proc_p,revis_p,temp_ens,tipo_il_p,nivel_il_p,mater_base,tipo_sec,num,ref,cod_enii,ancho,diam,vt,pt,tipo_pen,marca_kit,tiem_pen,met_rem,marca_kit1,tiem_sec,for_rev,marca_kit2,tiem_rev,equipo,modelo,iden) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(llave_form,fecha_form,proc,revis,nivel_il,con_sup,met_insp,tipo_il,check1,check2,check3,detalle,proc_p,revis_p,temp_ens,tipo_il_p,nivel_il_p,mater_base,tipo_sec,num,ref,cod_enii,ancho,diam,vt,pt,tipo_pen,marca_kit,tiem_pen,met_rem,marca_kit1,tiem_sec,for_rev,marca_kit2,tiem_rev,equipo,modelo,iden))
        mysql.connection.commit()
        return redirect(url_for('reporte_foto1'))
    return render_template('formu_1.html', form=form) 


@app.route('/formu_2', methods=['GET','POST'])
@login_required
def formu_2():
    form = formu2()
    if form.validate_on_submit():
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
        cur.execute("select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
        llave_form = cur.fetchone()
        cur.execute("select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
        fecha_form = cur.fetchone()
        cur.execute('insert into form3 (id_formulario,fec_formulario,proc,revis,nivel_il,con_sup,met_insp,tipo_il,check1,check2,check3,detalle,proc_p,revis_p,temp_ens,tipo_il_p,nivel_il_p,mater_base,tipo_sec,num,ref,cod_enii,vt,pt,tipo_pen,marca_kit,tiem_pen,met_rem,marca_kit1,tiem_sec,for_rev,marca_kit2,tiem_rev,equipo,modelo,iden,tipo_ter,medidas,capac,dia_elin,med_aces) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(llave_form,fecha_form,proc,revis,nivel_il,con_sup,met_insp,tipo_il,check1,check2,check3,detalle,proc_p,revis_p,temp_ens,tipo_il_p,nivel_il_p,mater_base,tipo_sec,num,ref,cod_enii,vt,pt,tipo_pen,marca_kit,tiem_pen,met_rem,marca_kit1,tiem_sec,for_rev,marca_kit2,tiem_rev,equipo,modelo,iden,tipo_ter,medidas,capac,dia_elin,med_aces))
        mysql.connection.commit()
        return redirect(url_for('reporte_foto1'))
    return render_template('formu_2.html', form=form) 




@app.route('/resumen')
@login_required
def resumen():
    cursor = mysql.connection.cursor()
    cursor.execute("select llave_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    nom_form = cursor.fetchone()
    cursor.execute("select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_insp = cursor.fetchone()
    cursor.execute("select fecha_emision_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_emi = cursor.fetchone()
    cursor.execute("select fecha_expiracion_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_exp = cursor.fetchone()
    cursor.execute("select lugar_ins_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    lugar = cursor.fetchone()
    cursor.execute("select nom_inspe_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    inpe = cursor.fetchone()
    return render_template('resumen.html', datos=nom_form, fec1=fec_insp, fec2=fec_emi,fec3=fec_exp,lugar=lugar,inspector=inpe)





@app.route('/servicios',methods=['GET','POST'])
def servicios():
    return render_template('servicios.html')
    


@app.route('/servicios/detalle/<slug>')
def servicios_detalle(slug):
    cursor = mysql.connection.cursor()
    cursor.execute(f"select * from empresa where slug='{slug}';")
    datos = cursor.fetchone()
    if datos==None: #si la consulta de la BD llega vacia
        return render_template('404.html')
    return render_template('detalle.html', datos=datos)


@app.route('/formulario_simple', methods=['GET','POST'])
def formulario_simple():
    if request.method=='POST':
        return f"email ={request.form['email']} | clave ={request.form['password']}"
    return render_template('formulario_simple.html')

@app.route('/formulario_simple_objeto', methods=['GET','POST'])
def formulario_simple_objeto():
    form = datos_reporte()
    if form.validate_on_submit():
        return f"email ={request.form['email']} | clave ={request.form['password']}"
    return render_template('formulario_simple_objeto.html', form=form)
        
  

@app.route('/caratula', methods=['GET','POST'])
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
        cur.execute("select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
        llave_form = cur.fetchone()
        cur.execute("select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
        fecha_form = cur.fetchone()
        cur.execute('insert into datos_equipo (id_formulario,fec_formulario,MARCA_datos_equipo,serie_datos_equipo,tipo_datos_equipo,modelo_datos_equipo,cap_datos_equipo,km_datos_equipo,anio_datos_equipo,codint_datos_equipo) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(llave_form,fecha_form,marca,serie,tipo,modelo,capacidad,kilometraje,anio,codigo))
        cur.execute('insert into datos_motor (id_formulario,fec_formulario,MARCA_Datos_Motor,SERIE_Datos_Motor,MODELO_Datos_Motor,HOROMETRO_Datos_Motor) VALUES (%s,%s,%s,%s,%s,%s)',(llave_form,fecha_form,marca_dm,serie_dm,modelo_dm,horometro_dm))
        cur.execute('insert into capacidad_trabajo (id_formulario,fec_formulario,CAP_MAX_Capacidad_Trabajo,LONG_PLUMA_Capacidad_Trabajo,RADIO_Capacidad_Trabajo,ANGULO_Capacidad_Trabajo) VALUES (%s,%s,%s,%s,%s,%s)',(llave_form,fecha_form,ct_capmax,ct_longpluma,ct_radio,ct_angulo))
        cur.execute('insert into datos_lmi (id_formulario,fec_formulario,FABRICANTE_DATOS_LMI,MARCA_DATOS_LMI,MODELO_DATOS_LMI,SERIE_DATOS_LMI) VALUES (%s,%s,%s,%s,%s,%s)',(llave_form,fecha_form,ct_lmi,ct_marca,ct_modelo,ct_serie))
        cur.execute('insert into pasteca_pri (id_formulario,fec_formulario,marca_pasteca_pri,capacidad_pasteca_pri,modelo_pasteca_pri,serie_ref_pasteca_pri,diacab_pasteca_pri) VALUES (%s,%s,%s,%s,%s,%s,%s)',(llave_form,fecha_form,pp_marca,pp_capacidad,pp_modelo,pp_serie_ref,pp_diam_clab))
        cur.execute('insert into pasteca_sec (id_formulario,fec_formulario,marca_pasteca_sec,capacidad_pasteca_sec,modelo_pasteca_sec,serie_ref_pasteca_sec,diacab_pasteca_sec) VALUES (%s,%s,%s,%s,%s,%s,%s)',(llave_form,fecha_form,ps_marca,ps_capacidad,ps_modelo,ps_serieref,ps_diam_clab))
        mysql.connection.commit()
        return render_template('CHECK_LIST_bck.html')
    return render_template('caratula.html', form=form) 


@app.route('/CHECK_LIST', methods=['GET','POST'])
@login_required
def CHECK_LIST_bck():
    
    return render_template('CHECK_LIST_bck.html')
   


@app.route('/check1',methods=['GET','POST'])
@login_required
def check1():
    cursor = mysql.connection.cursor()
    cursor.execute("select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    llave_form = cursor.fetchone()
    cursor.execute("select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    fecha_form = cursor.fetchone()
    form = check_list1()
    if form.validate_on_submit():
        valor = request.form.get('micheck')
        if valor == '7':
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Matricula Doc Identificación'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Manual de Operación'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Manual de servicio-partes'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Programa de Mantenimiento'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Registros de Reparaciones'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Tablas de Carga'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','File de certificaciones'))
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
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check1,'Matricula Doc Identificación',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check2,'Manual de Operación',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check3,'Manual de servicio-partes',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check4,'Programa de Mantenimiento',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check5,'Registros de Reparaciones',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check6,'Tablas de Carga',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check7,'File de certificaciones',checkobs))
            mysql.connection.commit()
            return redirect(url_for('check2'))
    return render_template('check1.html', dato=llave_form, form=form )

@app.route('/check2',methods=['GET','POST'])
@login_required
def check2():
    cursor = mysql.connection.cursor()
    cursor.execute("select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    llave_form = cursor.fetchone()
    cursor.execute("select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    fecha_form = cursor.fetchone()
    form = check_list2()
    if form.validate_on_submit():
        valor = request.form.get('micheck')
        if valor == '9':
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Accesos y puntos de apoyo, estado'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Puerta seguro posic. abierto y posic. cerrado'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Identificación de instrumentos y mandos'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Tipo de vidrio, parabrisas y techo'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Limpia parabrisas'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Cartilla de advertencia riesgo electrocución'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Estado de asiento, bloqueo posa brazo'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Cinturón de seguridad'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Condición de la cabina/estructura'))
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
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check1,'Accesos y puntos de apoyo, estado',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check2,'Puerta seguro posic. abierto y posic. cerrado',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check3,'Identificación de instrumentos y mandos',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check4,'Tipo de vidrio, parabrisas y techo',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check5,'Limpia parabrisas',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check6,'Cartilla de advertencia riesgo electrocución',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check7,'Estado de asiento, bloqueo posa brazo',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check8,'Cinturón de seguridad',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check9,'Condición de la cabina/estructura',checkobs))
            mysql.connection.commit()
            return redirect(url_for('check3'))
    return render_template('check2.html', dato=llave_form, form=form )

@app.route('/check3',methods=['GET','POST'])
@login_required
def check3():
    cursor = mysql.connection.cursor()
    cursor.execute("select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    llave_form = cursor.fetchone()
    cursor.execute("select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    fecha_form = cursor.fetchone()
    form = check_list3()
    if form.validate_on_submit():
        valor = request.form.get('micheck')
        if valor == '5':
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Accesos y puntos de apoyo, estado'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Puerta seguro posic. abierto y posic. cerrado'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Identificación de instrumentos y mandos'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Tipo de vidrio, parabrisas y techo'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Limpia parabrisas'))
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
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check1,'Accesos y puntos de apoyo, estado',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check2,'Puerta seguro posic. abierto y posic. cerrado',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check3,'Identificación de instrumentos y mandos',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check4,'Tipo de vidrio, parabrisas y techo',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check5,'Limpia parabrisas',checkobs))
            mysql.connection.commit()
            return redirect(url_for('check4'))
    return render_template('check3.html', dato=llave_form, form=form )

@app.route('/check4',methods=['GET','POST'])
@login_required
def check4():
    cursor = mysql.connection.cursor()
    cursor.execute("select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    llave_form = cursor.fetchone()
    cursor.execute("select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    fecha_form = cursor.fetchone()
    form = check_list4()
    if form.validate_on_submit():
        valor = request.form.get('micheck')
        if valor == '10':
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Luces Interiores de indicadores y de salón'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Faros frontales'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Direccionales delanteras'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Luz de parqueo'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Luz retro'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Luz de frenado'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Direccionales posteriores'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Licuadora (baliza)'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Alarma de retroceso'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Bocina'))
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
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check1,'Luces Interiores de indicadores y de salón',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check2,'Faros frontales',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check3,'Direccionales delanteras',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check4,'Luz de parqueo',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check5,'Luz retro',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check6,'Luz de frenado',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check7,'Direccionales posteriores',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check8,'Licuadora (baliza)',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check9,'Alarma de retroceso',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check10,'Bocina',checkobs))
            mysql.connection.commit()
            return redirect(url_for('check5'))
    return render_template('check4.html', dato=llave_form, form=form )

@app.route('/check5',methods=['GET','POST'])
@login_required
def check5():
    cursor = mysql.connection.cursor()
    cursor.execute("select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    llave_form = cursor.fetchone()
    cursor.execute("select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    fecha_form = cursor.fetchone()
    form = check_list5()
    if form.validate_on_submit():
        valor = request.form.get('micheck')
        if valor == '2':
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Fijaciones'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Características adecuadas'))
            mysql.connection.commit()
            return redirect(url_for('check6'))
        else:
            check1 = Text(form.check1.data)
            check2 = Text(form.check2.data)
            checkobs = Text(form.checkobs.data)
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check1,'Fijaciones',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check2,'Características adecuadas',checkobs))
            mysql.connection.commit()
            return redirect(url_for('check6'))
    return render_template('check5.html', dato=llave_form, form=form )


@app.route('/check6',methods=['GET','POST'])
@login_required
def check6():
    cursor = mysql.connection.cursor()
    cursor.execute("select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    llave_form = cursor.fetchone()
    cursor.execute("select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    fecha_form = cursor.fetchone()
    form = check_list6()
    if form.validate_on_submit():
        valor = request.form.get('micheck')
        if valor == '11':
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Indicador de longitud de boom'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Indicador de ángulo (mecánico)'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Indicador de ángulo (digital)'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Indicador de radio (digital)'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Antichoque de bloques winche prin.'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Antichoque de bloques winche Aux.'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Indicador de Carga, Capacidad, Limitador'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Limitador de elevación de pluma celosía'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Indicador de rotación del tambor'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Indicador de nivelación en cabina'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Indicador velocidad de viento'))
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
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check1,'Indicador de longitud de boom',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check2,'Indicador de ángulo (mecánico)',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check3,'Indicador de ángulo (digital)',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check4,'Indicador de radio (digital)',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check5,'Antichoque de bloques winche prin.',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check6,'Antichoque de bloques winche Aux.',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check7,'Indicador de Carga, Capacidad, Limitador',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check8,'Limitador de elevación de pluma celosía',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check9,'Indicador de rotación del tambor',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check10,'Indicador de nivelación en cabina',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check11,'Indicador velocidad de viento',checkobs))
            mysql.connection.commit()
            return redirect(url_for('check7'))
    return render_template('check6.html', dato=llave_form, form=form )

@app.route('/check7',methods=['GET','POST'])
@login_required
def check7():
    cursor = mysql.connection.cursor()
    cursor.execute("select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    llave_form = cursor.fetchone()
    cursor.execute("select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    fecha_form = cursor.fetchone()
    form = check_list7()
    if form.validate_on_submit():
        valor = request.form.get('micheck')
        if valor == '4':
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Extintor ABC'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Conos'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Adhesivos, señaléticas  de seguridad'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Superficie antideslizante'))
            mysql.connection.commit()
            return redirect(url_for('check8'))
        else:
            check1 = Text(form.check1.data)
            check2 = Text(form.check2.data)
            check3 = Text(form.check3.data)
            check4 = Text(form.check4.data)
            checkobs = Text(form.checkobs.data)
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check1,'Extintor ABC',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check2,'Conos',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check3,'Adhesivos, señaléticas  de seguridad',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check4,'Superficie antideslizante',checkobs))
            mysql.connection.commit()
            return redirect(url_for('check8'))
    return render_template('check7.html', dato=llave_form, form=form )


@app.route('/check8',methods=['GET','POST'])
@login_required
def check8():
    cursor = mysql.connection.cursor()
    cursor.execute("select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    llave_form = cursor.fetchone()
    cursor.execute("select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    fecha_form = cursor.fetchone()
    form = check_list8()
    if form.validate_on_submit():
        valor = request.form.get('micheck')
        if valor == '4':
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Estado del Chasis (bastidor)'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Estructura'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Soldaduras'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Vigas de estabilizadores'))
            mysql.connection.commit()
            return redirect(url_for('check9'))
        else:
            check1 = Text(form.check1.data)
            check2 = Text(form.check2.data)
            check3 = Text(form.check3.data)
            check4 = Text(form.check4.data)
            checkobs = Text(form.checkobs.data)
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check1,'Estado del Chasis (bastidor)',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check2,'Estructura',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check3,'Soldaduras',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check4,'Vigas de estabilizadores',checkobs))
            mysql.connection.commit()
            return redirect(url_for('check9'))
    return render_template('check8.html', dato=llave_form, form=form )

@app.route('/check9',methods=['GET','POST'])
@login_required
def check9():
    cursor = mysql.connection.cursor()
    cursor.execute("select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    llave_form = cursor.fetchone()
    cursor.execute("select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    fecha_form = cursor.fetchone()
    form = check_list9()
    if form.validate_on_submit():
        valor = request.form.get('micheck')
        if valor == '6':
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Condición de tramos'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Bases'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Soldadura'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Alineación'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Condición de Poleas'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Condición de Pasadores'))
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
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check1,'Condición de tramos',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check2,'Bases',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check3,'Soldadura',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check4,'Alineación',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check5,'Condición de Poleas',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check6,'Condición de Pasadores',checkobs))
            mysql.connection.commit()
            return redirect(url_for('check10'))
    return render_template('check9.html', dato=llave_form, form=form )

@app.route('/check10',methods=['GET','POST'])
@login_required
def check10():
    cursor = mysql.connection.cursor()
    cursor.execute("select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    llave_form = cursor.fetchone()
    cursor.execute("select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    fecha_form = cursor.fetchone()
    form = check_list10()
    if form.validate_on_submit():
        valor = request.form.get('micheck')
        if valor == '6':
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Condición de plumín'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Bases'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Soldadura'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Alineación'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Condición de Poleas'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Condición de Pasadores'))
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
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check1,'Condición de plumín',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check2,'Bases',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check3,'Soldadura',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check4,'Alineación',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check5,'Condición de Poleas',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check6,'Condición de Pasadores',checkobs))
            mysql.connection.commit()
            return redirect(url_for('check11'))
    return render_template('check10.html', dato=llave_form, form=form )

@app.route('/check11',methods=['GET','POST'])
@login_required
def check11():
    cursor = mysql.connection.cursor()
    cursor.execute("select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    llave_form = cursor.fetchone()
    cursor.execute("select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    fecha_form = cursor.fetchone()
    form = check_list11()
    if form.validate_on_submit():
        valor = request.form.get('micheck')
        if valor == '7':
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Cilindro(S) elevador de pluma'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Cilindro(S) estabilizadores'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Cilindro extensión pluma'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Cilindro(S) vigas de estabilizadores'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Circuito Hidráulico'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Winches'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Frenos'))
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
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check1,'Cilindro(S) elevador de pluma',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check2,'Cilindro(S) estabilizadores',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check3,'Cilindro extensión pluma',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check4,'Cilindro(S) vigas de estabilizadores',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check5,'Circuito Hidráulico',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check6,'Winches',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check7,'Frenos',checkobs))
            mysql.connection.commit()
            return redirect(url_for('check12'))
    return render_template('check11.html', dato=llave_form, form=form )

@app.route('/check12',methods=['GET','POST'])
@login_required
def check12():
    cursor = mysql.connection.cursor()
    cursor.execute("select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    llave_form = cursor.fetchone()
    cursor.execute("select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    fecha_form = cursor.fetchone()
    form = check_list12()
    if form.validate_on_submit():
        valor = request.form.get('micheck')
        if valor == '3':
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Compresor'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Líneas de conducción'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Acoples'))
            mysql.connection.commit()
            return redirect(url_for('check13'))
        else:
            check1 = Text(form.check1.data)
            check2 = Text(form.check2.data)
            check3 = Text(form.check3.data)
            checkobs = Text(form.checkobs.data)
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check1,'Compresor',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check2,'Líneas de conducción',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check3,'Acoples',checkobs))
            mysql.connection.commit()
            return redirect(url_for('check13'))
    return render_template('check12.html', dato=llave_form, form=form )

@app.route('/check13',methods=['GET','POST'])
@login_required
def check13():
    cursor = mysql.connection.cursor()
    cursor.execute("select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    llave_form = cursor.fetchone()
    cursor.execute("select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    fecha_form = cursor.fetchone()
    form = check_list13()
    if form.validate_on_submit():
        valor = request.form.get('micheck')
        if valor == '4':
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Cilindro(S) Estado de baterías'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Cilindro(S)Protección sobre carga eléctrica(fusibles)'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Interruptor Master'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Aislamiento de alambres y conectores'))
            mysql.connection.commit()
            return redirect(url_for('check14'))
        else:
            check1 = Text(form.check1.data)
            check2 = Text(form.check2.data)
            check3 = Text(form.check3.data)
            check4 = Text(form.check4.data)
            checkobs = Text(form.checkobs.data)
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check1,'Cilindro(S) Estado de baterías',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check2,'Cilindro(S)Protección sobre carga eléctrica(fusibles)',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check3,'Interruptor Master',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check4,'Aislamiento de alambres y conectores',checkobs))
            mysql.connection.commit()
            return redirect(url_for('check14'))
    return render_template('check13.html', dato=llave_form, form=form )

@app.route('/check14',methods=['GET','POST'])
@login_required
def check14():
    cursor = mysql.connection.cursor()
    cursor.execute("select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    llave_form = cursor.fetchone()
    cursor.execute("select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    fecha_form = cursor.fetchone()
    form = check_list14()
    if form.validate_on_submit():
        valor = request.form.get('micheck')
        if valor == '4':
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Mandos libres de atrapamientos'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Dirección del movimiento de mando'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Posición neutra de los mandos'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Señaléticas de funciones'))
            mysql.connection.commit()
            return redirect(url_for('check15'))
        else:
            check1 = Text(form.check1.data)
            check2 = Text(form.check2.data)
            check3 = Text(form.check3.data)
            check4 = Text(form.check4.data)
            checkobs = Text(form.checkobs.data)
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check1,'Mandos libres de atrapamientos',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check2,'Dirección del movimiento de mando',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check3,'Posición neutra de los mandos',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check4,'Señaléticas de funciones',checkobs))
            mysql.connection.commit()
            return redirect(url_for('check15'))
    return render_template('check14.html', dato=llave_form, form=form )

@app.route('/check15',methods=['GET','POST'])
@login_required
def check15():
    cursor = mysql.connection.cursor()
    cursor.execute("select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    llave_form = cursor.fetchone()
    cursor.execute("select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    fecha_form = cursor.fetchone()
    form = check_list15()
    if form.validate_on_submit():
        valor = request.form.get('micheck')
        if valor == '5':
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Cables estado estructural'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Lubricación'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Enrollado en el tambor'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Guarnido, del cable (trenzado)'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Terminal / socket / instalación'))
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
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check1,'Cables estado estructural',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check2,'Lubricación',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check3,'Enrollado en el tambor',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check4,'Guarnido, del cable (trenzado)',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check5,'Terminal / socket / instalación',checkobs))
            mysql.connection.commit()
            return redirect(url_for('check16'))
    return render_template('check15.html', dato=llave_form, form=form )

@app.route('/check16',methods=['GET','POST'])
@login_required
def check16():
    cursor = mysql.connection.cursor()
    cursor.execute("select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    llave_form = cursor.fetchone()
    cursor.execute("select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    fecha_form = cursor.fetchone()
    form = check_list16()
    if form.validate_on_submit():
        valor = request.form.get('micheck')
        if valor == '4':
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Ranuras'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Radio'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Bordes'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Holguras entre poleas y ejes'))
            mysql.connection.commit()
            return redirect(url_for('check17'))
        else:
            check1 = Text(form.check1.data)
            check2 = Text(form.check2.data)
            check3 = Text(form.check3.data)
            check4 = Text(form.check4.data)
            checkobs = Text(form.checkobs.data)
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check1,'Ranuras',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check2,'Radio',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check3,'Bordes',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check4,'Holguras entre poleas y ejes',checkobs))
            mysql.connection.commit()
            return redirect(url_for('check17'))
    return render_template('check16.html', dato=llave_form, form=form )

@app.route('/check17',methods=['GET','POST'])
@login_required
def check17():
    cursor = mysql.connection.cursor()
    cursor.execute("select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    llave_form = cursor.fetchone()
    cursor.execute("select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    fecha_form = cursor.fetchone()
    form = check_list17()
    if form.validate_on_submit():
        valor = request.form.get('micheck')
        if valor == '8':
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Marca de capacidad'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Marca de peso'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Giro del gancho'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','5% Abertura de garganta'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Desviación de la punta'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','10% Desgaste del gancho'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Seguro del gancho'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Estado del gancho'))
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
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check1,'Marca de capacidad',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check2,'Marca de peso',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check3,'Giro del gancho',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check4,'5% Abertura de garganta',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check5,'Desviación de la punta',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check6,'10% Desgaste del gancho',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check7,'Seguro del gancho',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check8,'Estado del gancho',checkobs))
            mysql.connection.commit()
            return redirect(url_for('check18'))
    return render_template('check17.html', dato=llave_form, form=form )


@app.route('/check18',methods=['GET','POST'])
@login_required
def check18():
    cursor = mysql.connection.cursor()
    cursor.execute("select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    llave_form = cursor.fetchone()
    cursor.execute("select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    fecha_form = cursor.fetchone()
    form = check_list18()
    if form.validate_on_submit():
        valor = request.form.get('micheck')
        if valor == '8':
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Marca de capacidad aux'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Marca de peso aux'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Giro del gancho aux'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','5% Abertura de garganta aux'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Desviación de la punta aux'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','10% Desgaste del gancho aux'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Seguro del gancho aux'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Estado del gancho aux'))
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
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check1,'Marca de capacidad aux',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check2,'Marca de peso aux',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check3,'Giro del gancho aux',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check4,'5% Abertura de garganta aux',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check5,'Desviación de la punta aux',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check6,'10% Desgaste del gancho aux',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check7,'Seguro del gancho aux',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check8,'Estado del gancho aux',checkobs))
            mysql.connection.commit()
            return redirect(url_for('check19'))
    return render_template('check18.html', dato=llave_form, form=form )


@app.route('/check19',methods=['GET','POST'])
@login_required
def check19():
    cursor = mysql.connection.cursor()
    cursor.execute("select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    llave_form = cursor.fetchone()
    cursor.execute("select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    fecha_form = cursor.fetchone()
    form = check_list19()
    if form.validate_on_submit():
        valor = request.form.get('micheck')
        if valor == '9':
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Accesos y puntos de apoyo'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Puerta seguro posic. abierto y posic. cerrado'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Vidrios, parabrisas y techo'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Limpia parabrisas'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Asiento'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Cinturón de seguridad'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Espejos laterales de cabina'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Fijación de volante'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Condición de la cabina/estructura'))
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
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check1,'Accesos y puntos de apoyo',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check2,'Puerta seguro posic. abierto y posic. cerrado',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check3,'Vidrios, parabrisas y techo',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check4,'Limpia parabrisas',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check5,'Asiento',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check6,'Cinturón de seguridad',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check7,'Espejos laterales de cabina',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check8,'Fijación de volante',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check9,'Condición de la cabina/estructura',checkobs))
            mysql.connection.commit()
            return redirect(url_for('check20'))
    return render_template('check19.html', dato=llave_form, form=form )

@app.route('/check20',methods=['GET','POST'])
@login_required
def check20():
    cursor = mysql.connection.cursor()
    cursor.execute("select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    llave_form = cursor.fetchone()
    cursor.execute("select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    fecha_form = cursor.fetchone()
    form = check_list20()
    if form.validate_on_submit():
        valor = request.form.get('micheck')
        if valor == '7':
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Estado del Chasis, soldadura'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Escape (guarda)'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Escaleras, manijas, guardas'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Suspensión, transmisión, dirección'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Fijación Pernos, espárragos, tuercas'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Alarma de retroceso'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Bocina'))
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
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check1,'Estado del Chasis, soldadura',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check2,'Escape (guarda)',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check3,'Escaleras, manijas, guardas',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check4,'Suspensión, transmisión, dirección',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check5,'Fijación Pernos, espárragos, tuercas',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check6,'Alarma de retroceso',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check7,'Bocina',checkobs))
            mysql.connection.commit()
            return redirect(url_for('check21'))
    return render_template('check20.html', dato=llave_form, form=form )

@app.route('/check21',methods=['GET','POST'])
@login_required
def check21():
    cursor = mysql.connection.cursor()
    cursor.execute("select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    llave_form = cursor.fetchone()
    cursor.execute("select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    fecha_form = cursor.fetchone()
    form = check_list21()
    if form.validate_on_submit():
        valor = request.form.get('micheck')
        if valor == '7':
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Neumáticos, apropiados según el fabricante'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Bandas de rodadura (neumáticos)'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Estructura (neumáticos)'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Tren de rodaje'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Zapatas (tren de rodaje)'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Rodillos (tren de rodaje)'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Catalinas (tren de rodaje)'))
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
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check1,'Neumáticos, apropiados según el fabricante',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check2,'Bandas de rodadura (neumáticos)',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check3,'Estructura (neumáticos)',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check4,'Tren de rodaje',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check5,'Zapatas (tren de rodaje)',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check6,'Rodillos (tren de rodaje)',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check7,'Catalinas (tren de rodaje)',checkobs))
            mysql.connection.commit()
            return redirect(url_for('check22'))
    return render_template('check21.html', dato=llave_form, form=form )

@app.route('/check22',methods=['GET','POST'])
@login_required
def check22():
    cursor = mysql.connection.cursor()
    cursor.execute("select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    llave_form = cursor.fetchone()
    cursor.execute("select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    fecha_form = cursor.fetchone()
    form = check_list22()
    if form.validate_on_submit():
        valor = request.form.get('micheck')
        if valor == '2':
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Gases de escape entubados'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Fugas de aceite por cuerpo del motor'))
            mysql.connection.commit()
            return redirect(url_for('check23'))
        else:
            check1 = Text(form.check1.data)
            check2 = Text(form.check2.data)
            checkobs = Text(form.checkobs.data)
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check1,'Gases de escape entubados',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check2,'Fugas de aceite por cuerpo del motor',checkobs))
            mysql.connection.commit()
            return redirect(url_for('check23'))
    return render_template('check22.html', dato=llave_form, form=form )

@app.route('/check23',methods=['GET','POST'])
@login_required
def check23():
    cursor = mysql.connection.cursor()
    cursor.execute("select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    llave_form = cursor.fetchone()
    cursor.execute("select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    fecha_form = cursor.fetchone()
    form = check_list23()
    if form.validate_on_submit():
        valor = request.form.get('micheck')
        if valor == '3':
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Tapa del combustible'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Conductos'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Deposito de combustible'))
            mysql.connection.commit()
            return redirect(url_for('check24'))
        else:
            check1 = Text(form.check1.data)
            check2 = Text(form.check2.data)
            check3 = Text(form.check3.data)
            checkobs = Text(form.checkobs.data)
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check1,'Tapa del combustible',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check2,'Conductos',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check3,'Deposito de combustible',checkobs))
            mysql.connection.commit()
            return redirect(url_for('check24'))
    
    return render_template('check23.html', dato=llave_form, form=form )

@app.route('/check24',methods=['GET','POST'])
@login_required
def check24():
    cursor = mysql.connection.cursor()
    cursor.execute("select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    llave_form = cursor.fetchone()
    cursor.execute("select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    fecha_form = cursor.fetchone()
    form = check_list24()
    if form.validate_on_submit():
        valor = request.form.get('micheck')
        if valor == '3':
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Pernos / tuercas'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Piñón, cremallera, dientes, guardas'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Pin / Seguro de tornamesa'))
            mysql.connection.commit()
            return redirect(url_for('check25'))
        else:
            check1 = Text(form.check1.data)
            check2 = Text(form.check2.data)
            check3 = Text(form.check3.data)
            checkobs = Text(form.checkobs.data)
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check1,'Pernos / tuercas',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check2,'Piñón, cremallera, dientes, guardas',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check3,'Pin / Seguro de tornamesa',checkobs))
            mysql.connection.commit()
            return redirect(url_for('check25'))

    return render_template('check24.html', dato=llave_form, form=form )


@app.route('/check25',methods=['GET','POST'])
@login_required
def check25():
    cursor = mysql.connection.cursor()
    cursor.execute("select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    llave_form = cursor.fetchone()
    cursor.execute("select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    fecha_form = cursor.fetchone()
    form = check_list25()
    if form.validate_on_submit():
        valor = request.form.get('micheck')
        if valor == '5':
            cur = mysql.connection.cursor()
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Mecanismos para levantar y bajar cargas'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Mecanismos para levantar y bajar pluma'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Mecanismo para extender y retraer pluma'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Mecanismo de giro'))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,'S','Mecanismo de viaje y/o recorrido'))
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
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check1,'Mecanismos para levantar y bajar cargas',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check2,'Mecanismos para levantar y bajar pluma',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check3,'Mecanismo para extender y retraer pluma',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check4,'Mecanismo de giro',checkobs))
            cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list,obs_check_list) VALUES (%s,%s,%s,%s,%s)',(llave_form,fecha_form,check5,'Mecanismo de viaje y/o recorrido',checkobs))
            mysql.connection.commit()
            return redirect(url_for('CHECK_FINAL'))


    return render_template('check25.html', dato=llave_form, form=form )


@app.route('/CHECK_FINAL',methods=['GET','POST'])
@login_required
def CHECK_FINAL():
    cursor = mysql.connection.cursor()
    cursor.execute("select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    llave_form = cursor.fetchone()
    cursor.execute("select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
    fecha_form = cursor.fetchone()
    form = CHECK_LIST_FIN()
    if form.validate_on_submit():
        check7 = Text(form.check7.data)
        cur = mysql.connection.cursor()
        cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,check7,'ZONA INSPECCIONADA'))
        cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,check7,'ENSAYO APLICADO'))
        cur.execute('insert into check_list (id_formulario,fecha_inspec_formulario,valor,nombre_check_list) VALUES (%s,%s,%s,%s)',(llave_form,fecha_form,check7,'REFERENCIA'))
        mysql.connection.commit()
        return redirect(url_for('PRUE_CARG'))
        
    return render_template('CHECK_FINAL.html', dato=llave_form, form=form )


@app.route('/REP_LMI', methods=['GET','POST'])
@login_required
def REP_LMI():
    form = datos_reporte()
    if form.validate_on_submit():
        return f"email ={request.form['email']} | clave ={request.form['password']}"
    return render_template('REP_LMI.html', form=form)

@app.route('/PRUE_CARG', methods=['GET','POST'])
@login_required
def PRUE_CARG():
    form = prueba_carga()
    print(form.errors)
    cursor = mysql.connection.cursor()
    cursor.execute("select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
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
        cursor.execute('insert into prue_carg_est (id_formulario,carga_utilizada,peso_carga,peso_aparejos,peso_total,medida,long_pluma,radio_ope,ang_pluma,cap_max,tiempo,carga,estab_1,estab_2,estab_3,estab_4) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(llave_form,p1,p2,p3,valor_t,'Kg',l_plu,r_oper,ang_plu,cap_max,'5',carga,est1,est2,est3,est4))
        cursor.execute('insert into prue_carg_est (id_formulario,carga_utilizada,peso_carga,peso_aparejos,peso_total,medida,long_pluma,radio_ope,ang_pluma,cap_max,tiempo,carga,estab_1,estab_2,estab_3,estab_4) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(llave_form,p1,p2,p3,valor_t,'Kg',l_plu,r_oper,ang_plu,cap_max,'5',carga2,est12,est22,est32,est42))
        cursor.execute('insert into prue_carg_est (id_formulario,carga_utilizada,peso_carga,peso_aparejos,peso_total,medida,long_pluma,radio_ope,ang_pluma,cap_max,tiempo,carga,estab_1,estab_2,estab_3,estab_4) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(llave_form,p1,p2,p3,valor_t,'Kg',l_plu,r_oper,ang_plu,cap_max,'5',carga3,est13,est23,est33,est43))
        mysql.connection.commit()
        return redirect('PRUE_CARG_3')  
    return render_template('PRUE_CARG.html', form=form)







@app.route('/PRUE_CARG_3', methods=['GET','POST'])
@login_required
def PRUE_CARG3():
    form = prueba_carga3()
    print(form.errors)
    cursor = mysql.connection.cursor()
    cursor.execute("select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario) ;")
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
        cursor.execute('insert into prue_carg_din (id_formulario,carga_utilizada,peso_carga,peso_aparejos,medida,peso_total,long_pluma,radio_ope,ang_pluma,cap_max,tornamesa,sis_mov_fre,est_estabilizado,cond_estab_maq) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(llave_form,p1,p2,p3,'Kg',valor_t,p5,p6,p7,p8,tor,tor1,tor2,tor3))
        mysql.connection.commit()
        return redirect('REP_FOTO_CARGA')
    return render_template('PRUE_CARG_3.html', form=form)





@app.route('/REP_FOTO_CARGA', methods=['GET','POST'])
@login_required
def REP_FOTO_CARGA():
    form= UploadForm() # carga request.from y request.file
    if form.validate_on_submit():
        f = form.photo.data
        filename = secure_filename(f.filename)
        f.save(app.root_path+"/static/img/subidas/"+filename)
        return redirect(url_for('inicio_foto'))
    return render_template('REP_FOTO_CARGA.html', form=form)


@app.route('/REP_FOTO', methods=['GET','POST'])
@login_required
def REP_FOTO():
    form= UploadForm() # carga request.from y request.file
    if form.validate_on_submit():
        f = form.photo.data
        filename = secure_filename(f.filename)
        f.save(app.root_path+"/static/img/subidas/"+filename)
        return redirect(url_for('reporte_foto'))
    return render_template('REP_FOTO.html', form=form)

@app.route('/RESULTADOS', methods=['GET', 'POST'])
@login_required
def RESULTADOS():
    #if request.method=="POST":
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
        number_of_rows_S=count_S[0]
        cursor.execute("select count(1) from check_list where valor ='DL' and id_formulario = (select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario));")
        count_DL = cursor.fetchone()
        number_of_rows_DL=count_DL[0]
        cursor.execute("select count(1) from check_list where valor ='DG' and id_formulario = (select id_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario));")
        count_DG = cursor.fetchone()
        number_of_rows_DG=count_DG[0]
        cursor.execute('insert into resultados (cod_ins,nom_ins,fecha_calib,id_formulario,DL_res,DG_res,S_res,conforme) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',(cod_int,'MULTIMETRO',fec_cal,id_f,number_of_rows_DL,number_of_rows_DG,number_of_rows_S,1))
        cursor.execute('insert into resultados (cod_ins,nom_ins,fecha_calib,id_formulario,DL_res,DG_res,S_res,conforme) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',(cod_int1,'CINTA METRICA',fec_cal1,id_f,number_of_rows_DL,number_of_rows_DG,number_of_rows_S,1))
        cursor.execute('insert into resultados (cod_ins,nom_ins,fecha_calib,id_formulario,DL_res,DG_res,S_res,conforme) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',(cod_int2,'PIE DE REY',fec_cal2,id_f,number_of_rows_DL,number_of_rows_DG,number_of_rows_S,1))
        cursor.execute('insert into resultados (cod_ins,nom_ins,fecha_calib,id_formulario,DL_res,DG_res,S_res,conforme) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',(cod_int3,'FLEXOMETRO',fec_cal3,id_f,number_of_rows_DL,number_of_rows_DG,number_of_rows_S,1))
        cursor.execute('insert into resultados (cod_ins,nom_ins,fecha_calib,id_formulario,DL_res,DG_res,S_res,conforme) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',(cod_int4,'GONIOMETRO',fec_cal4,id_f,number_of_rows_DL,number_of_rows_DG,number_of_rows_S,1))
        mysql.connection.commit()
        if number_of_rows_DG >= 1:
            cond = 'EQUIPO NO CONFORME'
            return render_template('RESULTADOS.html', a=cod_int, fec1=fec_cal, b=cod_int1,fec2=fec_cal1,
                                c=cod_int2,fec3=fec_cal2,d=cod_int3,fec4=fec_cal3,e=cod_int4,
                                fec5=fec_cal4,S=count_S,DL=count_DL,DG=count_DG,C=cond,id_f=id_f)
        if number_of_rows_DL >=0 and number_of_rows_DG ==0:
            cond = 'EQUIPO CONFORME CON DEFECTOS LEVES'
            return render_template('RESULTADOS.html', a=cod_int, fec1=fec_cal, b=cod_int1,fec2=fec_cal1,
                                    c=cod_int2,fec3=fec_cal2,d=cod_int3,fec4=fec_cal3,e=cod_int4,
                                    fec5=fec_cal4,S=count_S,DL=count_DL,DG=count_DG,C=cond,id_f=id_f)
        cond = 'EQUIPO CONFORME'    
        return render_template('RESULTADOS.html', a=cod_int, fec1=fec_cal, b=cod_int1,fec2=fec_cal1,
                                c=cod_int2,fec3=fec_cal2,d=cod_int3,fec4=fec_cal3,e=cod_int4,fec5=fec_cal4,
                                S=count_S,DL=count_DL,DG=count_DG,C=cond,id_f=id_f)
        


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
    


@app.route('/CERTIFICADO_GM', methods=['GET','POST'])
@login_required
def CERTIFICADO_GM():
    cursor = mysql.connection.cursor()
    cursor.execute("select llave_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    nom_form = cursor.fetchone()
    cursor.execute("select fecha_inspec_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_insp = cursor.fetchone()
    cursor.execute("select fecha_emision_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_emi = cursor.fetchone()
    cursor.execute("select fecha_expiracion_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    fec_exp = cursor.fetchone()
    cursor.execute("select lugar_ins_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    lugar = cursor.fetchone()
    cursor.execute("select nom_inspe_formulario from formulario where id_formulario = (select MAX(id_formulario) from formulario);")
    inpe = cursor.fetchone()
    cursor.execute("select codint_datos_equipo from datos_equipo where id_formulario = (select MAX(id_formulario) from formulario);")
    cod_inter = cursor.fetchone()
    cursor.execute("select CAP_MAX_Capacidad_Trabajo from capacidad_trabajo where id_formulario = (select MAX(id_formulario) from formulario);")
    cap_max = cursor.fetchone()
    cursor.execute("select modelo_datos_equipo from datos_equipo where id_formulario = (select MAX(id_formulario) from formulario);")
    modelo = cursor.fetchone()
    cursor.execute("select MARCA_datos_equipo from datos_equipo where id_formulario = (select MAX(id_formulario) from formulario);")
    marca = cursor.fetchone()
    cursor.execute("select anio_datos_equipo from datos_equipo where id_formulario = (select MAX(id_formulario) from formulario);")
    ani = cursor.fetchone()
    cursor.execute("select serie_datos_equipo from datos_equipo where id_formulario = (select MAX(id_formulario) from formulario);")
    serie = cursor.fetchone()
    cursor.execute("select cod_ins from resultados where nom_ins = 'MULTIMETRO' and id_formulario = (select MAX(id_formulario) from formulario);")
    cod1 = cursor.fetchone()
    cursor.execute("select nom_ins from resultados where nom_ins = 'MULTIMETRO' and id_formulario = (select MAX(id_formulario) from formulario);")
    nom1 = cursor.fetchone()
    cursor.execute("select fecha_calib from resultados where nom_ins = 'MULTIMETRO' and id_formulario = (select MAX(id_formulario) from formulario);")
    fec_cal1 = cursor.fetchone()
    cursor.execute("select cod_ins from resultados where nom_ins = 'CINTA METRICA' and id_formulario = (select MAX(id_formulario) from formulario);")
    cod2 = cursor.fetchone()
    cursor.execute("select nom_ins from resultados where nom_ins = 'CINTA METRICA' and id_formulario = (select MAX(id_formulario) from formulario);")
    nom2 = cursor.fetchone()
    cursor.execute("select fecha_calib from resultados where nom_ins = 'CINTA METRICA' and id_formulario = (select MAX(id_formulario) from formulario);")
    fec_cal2 = cursor.fetchone()
    cursor.execute("select cod_ins from resultados where nom_ins = 'PIE DE REY' and id_formulario = (select MAX(id_formulario) from formulario);")
    cod3 = cursor.fetchone()
    cursor.execute("select nom_ins from resultados where nom_ins = 'PIE DE REY' and id_formulario = (select MAX(id_formulario) from formulario);")
    nom3 = cursor.fetchone()
    cursor.execute("select fecha_calib from resultados where nom_ins = 'PIE DE REY' and id_formulario = (select MAX(id_formulario) from formulario);")
    fec_cal3 = cursor.fetchone()
    cursor.execute("select cod_ins from resultados where nom_ins = 'FLEXOMETRO' and id_formulario = (select MAX(id_formulario) from formulario);")
    cod4 = cursor.fetchone()
    cursor.execute("select nom_ins from resultados where nom_ins = 'FLEXOMETRO' and id_formulario = (select MAX(id_formulario) from formulario);")
    nom4 = cursor.fetchone()
    cursor.execute("select fecha_calib from resultados where nom_ins = 'FLEXOMETRO' and id_formulario = (select MAX(id_formulario) from formulario);")
    fec_cal4 = cursor.fetchone()
    cursor.execute("select cod_ins from resultados where nom_ins = 'GONIOMETRO' and id_formulario = (select MAX(id_formulario) from formulario);")
    cod5 = cursor.fetchone()
    cursor.execute("select nom_ins from resultados where nom_ins = 'GONIOMETRO' and id_formulario = (select MAX(id_formulario) from formulario);")
    nom5 = cursor.fetchone()
    cursor.execute("select fecha_calib from resultados where nom_ins = 'GONIOMETRO' and id_formulario = (select MAX(id_formulario) from formulario);")
    fec_cal5 = cursor.fetchone()
    
    return render_template('CERTIFICADO_GM.html', datos=nom_form, 
                            fec1=fec_insp, fec2=fec_emi,fec3=fec_exp,lugar=lugar,inspector=inpe, 
                            cod_inter=cod_inter,cap_max=cap_max,modelo=modelo,marca=marca,ani=ani,
                            serie=serie,cod1=cod1,nom1=nom1,fec_cal1=fec_cal1,cod2=cod2,nom2=nom2,
                            fec_cal2=fec_cal2,cod3=cod3,nom3=nom3,fec_cal3=fec_cal3,cod4=cod4,nom4=nom4,
                            fec_cal4=fec_cal4,cod5=cod5,nom5=nom5,fec_cal5=fec_cal5)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("error.html", error="Página no encontrada..."), 404

@app.route('/cons_404', methods=['GET','POST'])
def cons_404():
    return render_template('404_cons.html')


@app.route('/login', methods=['get', 'post'])
def login():
    from aplicacion.models import Usuarios
    # Control de permisos
    if current_user.is_authenticated:
        #return 'OK'
        return redirect(url_for("inicio_1"))
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
            return redirect(next or url_for('inicio_1'))
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


