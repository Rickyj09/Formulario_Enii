from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, IntegerField,\
    TextAreaField, SelectField, PasswordField
from wtforms.fields.html5 import EmailField
from flask_wtf.file import FileField
from wtforms.validators import Required
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, FileField, SelectField,RadioField
from wtforms import FloatField
from wtforms.validators import DataRequired, Email, Length, ValidationError,AnyOf
from wtforms.fields.html5 import DateField
from flask_wtf.file import FileField, FileRequired
from wtforms.fields.html5 import EmailField
from wtforms.validators import Required

def validar_obvio(form,field):
    if field.data=="12345678":
        raise ValidationError('La clave debe ser más segura!!')

class Publicaciones(FlaskForm):
    post = TextAreaField('Notas de las fotos', validators=[
        DataRequired(), Length(min=1, max=140)
    ])
    imagen = FileField('image')
 
    submit = SubmitField('Subir')

class FormArticulo(FlaskForm):
    nombre = StringField("Nombre:",
                         validators=[Required("Tienes que introducir el dato")]
                         )
    precio = DecimalField("Precio:", default=0,
                          validators=[Required("Tienes que introducir el dato")
                                      ])
    iva = IntegerField("IVA:", default=21,
                       validators=[Required("Tienes que introducir el dato")])
    descripcion = TextAreaField("Descripción:")
    photo = FileField('Selecciona imagen:')
    stock = IntegerField("Stock:", default=1,
                         validators=[Required("Tienes que introducir el dato")]
                         )
    CategoriaId = SelectField("Categoría:", coerce=int)
    submit = SubmitField('Enviar')

class FormSINO(FlaskForm):
    si = SubmitField('Si')
    no = SubmitField('No')


class LoginForm(FlaskForm):
    username = StringField('User', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])
    submit = SubmitField('Entrar')


class FormUsuario(FlaskForm):
    username = StringField('Login', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])
    nombre = StringField('Nombre completo')
    email = EmailField('Email')
    submit = SubmitField('Aceptar')


class datos_equipo(FlaskForm):
    de_marca = StringField('MARCA', validators=[DataRequired()],render_kw={"placeholder": "Marca"})
    de_serie = StringField('SERIE', validators=[DataRequired()])
    de_tipo = StringField('TIPO', validators=[DataRequired()])
    de_modelo = StringField('MODELO', validators=[DataRequired()])
    de_capacidad = StringField('CAPACIDAD', validators=[DataRequired()])
    de_kilometraje = StringField('KILOMETRAJE', validators=[DataRequired()])
    de_anio = StringField('AÑO', validators=[DataRequired()])
    de_cod_interno = StringField('CODIGO INTERNO', validators=[DataRequired()])
    dm_marca =  StringField('MARCA', validators=[DataRequired()])
    dm_serie = StringField('SERIE', validators=[DataRequired()])
    dm_modelo = StringField('MODELO', validators=[DataRequired()])
    dm_horometro = StringField('HORÓMETRO', validators=[DataRequired()])
    ct_capmax = StringField('CAPACIDAD MAXIMA', validators=[DataRequired()])
    ct_longpluma = StringField('LONG PLUMA', validators=[DataRequired()])
    ct_radio = StringField('RADIO', validators=[DataRequired()])
    ct_angulo = StringField('ANGULO', validators=[DataRequired()])
    ct_lmi = StringField('FABRICANTE', validators=[DataRequired()])
    ct_marca = StringField('MARCA', validators=[DataRequired()])
    ct_modelo = StringField('MODELO', validators=[DataRequired()])
    ct_serie = StringField('SERIE/REFERENCIA', validators=[DataRequired()])
    pp_marca = StringField('MARCA', validators=[DataRequired()])
    pp_capacidad = StringField('CAPACIDAD ', validators=[DataRequired()])
    pp_modelo = StringField('MODELO', validators=[DataRequired()])
    pp_serie_ref = StringField('SERIE/REFERENCIA', validators=[DataRequired()])
    pp_diam_clab = StringField('DIAMETRO DE CABLE', validators=[DataRequired()])
    ps_marca = StringField('MARCA', validators=[DataRequired()])
    ps_capacidad = StringField('CAPACIDAD ', validators=[DataRequired()])
    ps_modelo = StringField('MODELO', validators=[DataRequired()])
    ps_serieref = StringField('SERIE/REFERENCIA', validators=[DataRequired()])
    ps_diam_clab = StringField('DIAMETRO DE CABLE', validators=[DataRequired()])
    conf_caratula = RadioField('', choices=[('c', 'Conforme'), ('NC', 'No Conforme')],default = 'C',render_kw={}, id='conf_caratula')

    submit = SubmitField('Enviar')


class formu1(FlaskForm):
    proc = StringField('PROCEDIMIENTO Nº', validators=[DataRequired()],render_kw={"placeholder": "PROCEDIMIENTO Nº"})
    revis = StringField('REVISIÓN Nº', validators=[DataRequired()])
    nivel_il = StringField('NIVEL DE ILUMINACIÓN:', validators=[DataRequired()])
    con_sup = StringField('CONDICIÓN SUPERFICIAL:', validators=[DataRequired()])
    met_insp = StringField('MÉTODO DE INSPECCIÓN:', validators=[DataRequired()])
    tipo_il = StringField('TIPO DE ILUMINACIÓN:', validators=[DataRequired()])
    check1 = RadioField('ESPEJOS:',choices=[('S', 'Satisfactorio')], id='check1')
    check2 = RadioField('LENTES:',choices=[('S', 'Satisfactorio')], id='check2')
    check3 = RadioField('OTROS:',choices=[('S', 'Satisfactorio')], id='check3')
    detalle = StringField('Detalla:', validators=[])
    proc_p =  StringField('PROCEDIMIENTO Nº', validators=[DataRequired()])
    revis_p = StringField('REVISIÓN Nº', validators=[DataRequired()])
    temp_ens = StringField('TEMPERATURA DE ENSAYO', validators=[DataRequired()])
    tipo_il_p = StringField('TIPO DE ILUMINACIÓN', validators=[DataRequired()])
    nivel_il_p = StringField('NIVEL DE ILUMINACIÓN', validators=[DataRequired()])
    mater_base = StringField('MATERIAL BASE', validators=[DataRequired()])
    tipo_sec = StringField('TIPO DE SECADO', validators=[DataRequired()])
    num = StringField('Nº', validators=[DataRequired()])
    ref = StringField('REFERENCIA', validators=[DataRequired()])
    cod_enii = StringField('CÓDIGO ENII', validators=[DataRequired()])
    ancho = StringField('ANCHO (mm)', validators=[DataRequired()])
    diam = StringField('DIÁMETRO (mm)', validators=[DataRequired()])
    vt = RadioField('INSPECCIÓN VISUAL (VT)',choices=[('A', 'Aprobado'), ('R', 'Rechazado')],default = 'A', id='vt')
    pt = RadioField('LÍQUIDOS PENETRANTES (PT)',choices=[('A', 'Aprobado'), ('R', 'Rechazado')],default = 'A', id='pt')
    
    submit = SubmitField('Enviar')

class CHECK_LIST():
    submit = SubmitField('Grabar')


class check_list1(FlaskForm):
    check1 = RadioField('1.- Matricula Doc Identificación',choices=[('S', 'Satisfactorio'), ('DL', 'Defecto Leve')],default = 'S', id='check1')
    check2 = RadioField('2. Manual de Operación', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check2')
    check3 = RadioField('3. Manual de servicio-partes', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check3')
    check4 = RadioField('4. Programa de Mantenimiento', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check4')
    check5 = RadioField('5. Registros de Reparaciones', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave'),('NA', 'No Aplica')],default = 'S',render_kw={}, id='check5')
    check6 = RadioField('6. Tablas de Carga', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check6')
    check7 = RadioField('7. File de certificaciones', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check7')
    checkobs = TextAreaField('OBSERVACIONES', validators=[],render_kw={},id='observaciones')
    

    submit = SubmitField('Grabar')


class check_list2(FlaskForm):
    check1 = RadioField(u'CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check1')
    check2 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check2')
    check3 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check3')
    check4 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check4')
    check5 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check5')
    check6 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check6')
    check7 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check7')
    check8 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check8')
    check9 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check9')
    checkobs = TextAreaField('OBSERVACIONES', validators=[],render_kw={},id='observaciones')
    
    submit = SubmitField('Grabar')

class check_list3(FlaskForm):
    check1 = RadioField(u'CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave'),('NA','No Aplica')],default = 'S',render_kw={}, id='check1')
    check2 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave'),('NA','No Aplica')],default = 'S',render_kw={}, id='check2')
    check3 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave'),('NA','No Aplica')],default = 'S',render_kw={}, id='check3')
    check4 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave'),('NA','No Aplica')],default = 'S',render_kw={}, id='check4')
    check5 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave'),('NA','No Aplica')],default = 'S',render_kw={}, id='check5')
    checkobs = TextAreaField('OBSERVACIONES', validators=[],render_kw={},id='observaciones')  

    submit = SubmitField('Grabar')

class check_list4(FlaskForm):
    check1 = RadioField(u'CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DL', 'Defecto Leve'),('NA','No Aplica')],default = 'S',render_kw={}, id='check1')
    check2 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave'),('NA','No Aplica')],default = 'S',render_kw={}, id='check2')
    check3 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave'),('NA','No Aplica')],default = 'S',render_kw={}, id='check3')
    check4 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave'),('NA','No Aplica')],default = 'S',render_kw={}, id='check4')
    check5 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave'),('NA','No Aplica')],default = 'S',render_kw={}, id='check5')
    check6 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave'),('NA','No Aplica')],default = 'S',render_kw={}, id='check6')
    check7 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave'),('NA','No Aplica')],default = 'S',render_kw={}, id='check7')
    check8 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DL', 'Defecto Leve'),('NA','No Aplica')],default = 'S',render_kw={}, id='check8')
    check9 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check9')
    check10 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check10')
    checkobs = TextAreaField('OBSERVACIONES', validators=[],render_kw={},id='observaciones')
    
    submit = SubmitField('Grabar')

class check_list5(FlaskForm):
    check1 = RadioField(u'CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave'),('NA','No Aplica')],default = 'S',render_kw={}, id='check1')
    check2 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave'),('NA','No Aplica')],default = 'S',render_kw={}, id='check2')
    checkobs = TextAreaField('OBSERVACIONES', validators=[],render_kw={},id='observaciones')
    
    submit = SubmitField('Grabar')

class check_list6(FlaskForm):
    check1 = RadioField(u'CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave'),('NA','No Aplica')],default = 'S',render_kw={}, id='check1')
    check2 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave'),('NA','No Aplica')],default = 'S',render_kw={}, id='check2')
    check3 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave'),('NA','No Aplica')],default = 'S',render_kw={}, id='check3')
    check4 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave'),('NA','No Aplica')],default = 'S',render_kw={}, id='check4')
    check5 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave'),('NA','No Aplica')],default = 'S',render_kw={}, id='check5')
    check6 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave'),('NA','No Aplica')],default = 'S',render_kw={}, id='check6')
    check7 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave'),('NA','No Aplica')],default = 'S',render_kw={}, id='check7')
    check8 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave'),('NA','No Aplica')],default = 'S',render_kw={}, id='check8')
    check9 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DL', 'Defecto Leve'),('NA','No Aplica')],default = 'S',render_kw={}, id='check9')
    check10 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check10')
    check11 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave'),('NA','No Aplica')],default = 'S',render_kw={}, id='check11')
    checkobs = TextAreaField('OBSERVACIONES', validators=[],render_kw={},id='observaciones')
    
    submit = SubmitField('Grabar')

class check_list7(FlaskForm):
    check1 = RadioField(u'CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DL', 'Defecto Leve')],default = 'S',render_kw={}, id='check1')
    check2 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DL', 'Defecto Leve')],default = 'S',render_kw={}, id='check2')
    check3 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check3')
    check4 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check4')
    checkobs = TextAreaField('OBSERVACIONES', validators=[],render_kw={},id='observaciones')  

    submit = SubmitField('Grabar')

   

class check_list8(FlaskForm):
    check1 = RadioField(u'CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check1')
    check2 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check2')
    check3 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check3')
    check4 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave'),('NA','No Aplica')],default = 'S',render_kw={}, id='check4')
    checkobs = TextAreaField('OBSERVACIONES', validators=[],render_kw={},id='observaciones') 

    submit = SubmitField('Grabar')

class check_list9(FlaskForm):
    check1 = RadioField(u'CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check1')
    check2 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check2')
    check3 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check3')
    check4 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check4')
    check5 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check5')
    check6 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check6')
    checkobs = TextAreaField('OBSERVACIONES', validators=[],render_kw={},id='observaciones')

    submit = SubmitField('Grabar')  

class check_list10(FlaskForm):
    check1 = RadioField(u'CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check1')
    check2 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check2')
    check3 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check3')
    check4 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check4')
    check5 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check5')
    check6 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check6')
    checkobs = TextAreaField('OBSERVACIONES', validators=[],render_kw={},id='observaciones') 

    submit = SubmitField('Grabar')

class check_list11(FlaskForm):
    check1 = RadioField(u'CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave'),('NA','No Aplica')],default = 'S',render_kw={}, id='check1')
    check2 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave'),('NA','No Aplica')],default = 'S',render_kw={}, id='check2')
    check3 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave'),('NA','No Aplica')],default = 'S',render_kw={}, id='check3')
    check4 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave'),('NA','No Aplica')],default = 'S',render_kw={}, id='check4')
    check5 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check5')
    check6 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check6')
    check7 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check7')
    checkobs = TextAreaField('OBSERVACIONES', validators=[],render_kw={},id='observaciones')

    submit = SubmitField('Grabar')


class check_list12(FlaskForm):
    check1 = RadioField(u'CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check1')
    check2 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check2')
    check3 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check3')
    checkobs = TextAreaField('OBSERVACIONES', validators=[],render_kw={},id='observaciones')

    submit = SubmitField('Grabar')

class check_list13(FlaskForm):
    check1 = RadioField(u'CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check1')
    check2 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check2')
    check3 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check3')
    check4 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check4')
    checkobs = TextAreaField('OBSERVACIONES', validators=[],render_kw={},id='observaciones')

    submit = SubmitField('Grabar')

class check_list14(FlaskForm):
    check1 = RadioField(u'CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check1')
    check2 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check2')
    check3 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check3')
    check4 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DL', 'Defecto Leve')],default = 'S',render_kw={}, id='check4')
    checkobs = TextAreaField('OBSERVACIONES', validators=[],render_kw={},id='observaciones')

    submit = SubmitField('Grabar')

class check_list15(FlaskForm):
    check1 = RadioField(u'CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check1')
    check2 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DL', 'Defecto Leve')],default = 'S',render_kw={}, id='check2')
    check3 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check3')
    check4 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check4')
    check5 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check5')
    checkobs = TextAreaField('OBSERVACIONES', validators=[],render_kw={},id='observaciones')

    submit = SubmitField('Grabar')

class check_list16(FlaskForm):
    check1 = RadioField(u'CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check1')
    check2 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check2')
    check3 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check3')
    check4 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check4')
    checkobs = TextAreaField('OBSERVACIONES', validators=[],render_kw={},id='observaciones')

    submit = SubmitField('Grabar')

class check_list17(FlaskForm):
    check1 = RadioField(u'CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check1')
    check2 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check2')
    check3 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check3')
    check4 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check4')
    check5 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check5')
    check6 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check6')
    check7 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check7')
    check8 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check8')
    checkobs = TextAreaField('OBSERVACIONES', validators=[],render_kw={},id='observaciones')
   
    submit = SubmitField('Grabar')

class check_list18(FlaskForm):
    check1 = RadioField(u'CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave'),('NA','No Aplica')],default = 'S',render_kw={}, id='check1')
    check2 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave'),('NA','No Aplica')],default = 'S',render_kw={}, id='check2')
    check3 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave'),('NA','No Aplica')],default = 'S',render_kw={}, id='check3')
    check4 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave'),('NA','No Aplica')],default = 'S',render_kw={}, id='check4')
    check5 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave'),('NA','No Aplica')],default = 'S',render_kw={}, id='check5')
    check6 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave'),('NA','No Aplica')],default = 'S',render_kw={}, id='check6')
    check7 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave'),('NA','No Aplica')],default = 'S',render_kw={}, id='check7')
    check8 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave'),('NA','No Aplica')],default = 'S',render_kw={}, id='check8')
    checkobs = TextAreaField('OBSERVACIONES', validators=[],render_kw={},id='observaciones')
   
   
    submit = SubmitField('Grabar')



class check_list19(FlaskForm):
    check1 = RadioField(u'CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave'),('NA','No Aplica')],default = 'S',render_kw={}, id='check1')
    check2 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave'),('NA','No Aplica')],default = 'S',render_kw={}, id='check2')
    check3 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave'),('NA','No Aplica')],default = 'S',render_kw={}, id='check3')
    check4 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave'),('NA','No Aplica')],default = 'S',render_kw={}, id='check4')
    check5 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DL', 'Defecto Leve'),('NA','No Aplica')],default = 'S',render_kw={}, id='check5')
    check6 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave'),('NA','No Aplica')],default = 'S',render_kw={}, id='check6')
    check7 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DL', 'Defecto Leve'),('NA','No Aplica')],default = 'S',render_kw={}, id='check7')
    check8 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave'),('NA','No Aplica')],default = 'S',render_kw={}, id='check8')
    check9 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave'),('NA','No Aplica')],default = 'S',render_kw={}, id='check9')
    checkobs = TextAreaField('OBSERVACIONES', validators=[],render_kw={},id='observaciones')


    submit = SubmitField('Grabar')

class check_list20(FlaskForm):
    check1 = RadioField(u'CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave'),('NA','No Aplica')],default = 'S',render_kw={}, id='check1')
    check2 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave'),('NA','No Aplica')],default = 'S',render_kw={}, id='check2')
    check3 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave'),('NA','No Aplica')],default = 'S',render_kw={}, id='check3')
    check4 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave'),('NA','No Aplica')],default = 'S',render_kw={}, id='check4')
    check5 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave'),('NA','No Aplica')],default = 'S',render_kw={}, id='check5')
    check6 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave'),('NA','No Aplica')],default = 'S',render_kw={}, id='check6')
    check7 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave'),('NA','No Aplica')],default = 'S',render_kw={}, id='check7')
    checkobs = TextAreaField('OBSERVACIONES', validators=[],render_kw={},id='observaciones')
        
    submit = SubmitField('Grabar')

class check_list21(FlaskForm):
    check1 = RadioField(u'CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave'),('NA','No Aplica')],default = 'S',render_kw={}, id='check1')
    check2 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave'),('NA','No Aplica')],default = 'S',render_kw={}, id='check2')
    check3 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave'),('NA','No Aplica')],default = 'S',render_kw={}, id='check3')
    check4 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave'),('NA','No Aplica')],default = 'S',render_kw={}, id='check4')
    check5 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave'),('NA','No Aplica')],default = 'S',render_kw={}, id='check5')
    check6 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave'),('NA','No Aplica')],default = 'S',render_kw={}, id='check6')
    check7 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave'),('NA','No Aplica')],default = 'S',render_kw={}, id='check7')
    checkobs = TextAreaField('OBSERVACIONES', validators=[],render_kw={},id='observaciones')
    
    submit = SubmitField('Grabar')


class check_list22(FlaskForm):
    check1 = RadioField(u'CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check1')
    check2 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check2')
    checkobs = TextAreaField('OBSERVACIONES', validators=[],render_kw={},id='observaciones')
        
    submit = SubmitField('Grabar')

class check_list23(FlaskForm):
    check1 = RadioField(u'CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check1')
    check2 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check2')
    check3 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check3')
    checkobs = TextAreaField('OBSERVACIONES', validators=[],render_kw={},id='observaciones')
        
    submit = SubmitField('Grabar')


class check_list24(FlaskForm):
    check1 = RadioField(u'CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check1')
    check2 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check2')
    check3 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check3')
    checkobs = TextAreaField('OBSERVACIONES', validators=[],render_kw={},id='observaciones')
        
    submit = SubmitField('Grabar')


class check_list25(FlaskForm):
    check1 = RadioField(u'CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check1')
    check2 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check2')
    check3 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave'),('NA','No Aplica')],default = 'S',render_kw={}, id='check3')
    check4 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check4')
    check5 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check5')
    checkobs = TextAreaField('OBSERVACIONES', validators=[],render_kw={},id='observaciones')
        
    submit = SubmitField('Grabar')


class CHECK_LIST_FIN(FlaskForm):
    check1 = StringField('ZONA INSPECCIONADA ', validators=[],render_kw={})
    check2 = StringField('ENSAYO APLICADO', validators=[],render_kw={})
    check3 = StringField('REFERENCIA', validators=[],render_kw={})
    check4 = StringField('ZONA INSPECCIONADA ', validators=[],render_kw={})
    check5 = StringField('ENSAYO APLICADO', validators=[],render_kw={})
    check6 = StringField('REFERENCIA', validators=[],render_kw={})
    check7 = RadioField('CONDICIÓN', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check4')

    submit = SubmitField('Grabar')


class prueba_carga(FlaskForm):
    conforme = RadioField('',choices=[('c', 'Conforme'),('nc','No Conforme')],render_kw={}, id='conforme')
    carga_utli_est = FloatField('CARGA UTILIZADA',validators=[DataRequired()])
    peso_carga_est = FloatField('PESO CARGA',validators=[DataRequired()])
    peso_aparejo_est = FloatField('PESO APAREJOS',validators=[DataRequired()])
    peso_total = FloatField('PESO TOTAL')
    long_pluma_est = FloatField('Longitud Pluma',validators=[DataRequired()])
    rad_oper_est = FloatField('Radio de Operación',validators=[DataRequired()])
    ang_pluma_est = FloatField('Angulo de Pluma (°)',validators=[DataRequired()])
    cap_maxima_est = FloatField('Capacidad Máxima',validators=[DataRequired()])
    carga = FloatField('Carga',validators=[DataRequired()])
    ESTAB1 = FloatField('ESTAB. 1',validators=[DataRequired()])
    ESTAB2 = FloatField('ESTAB. 2',validators=[DataRequired()])
    ESTAB3 = FloatField('ESTAB. 3',validators=[DataRequired()])
    ESTAB4 = FloatField('ESTAB. 4',validators=[DataRequired()])
    carga2 = FloatField('Carga',validators=[DataRequired()])
    ESTAB12 = FloatField('ESTAB. 1',validators=[DataRequired()])
    ESTAB22 = FloatField('ESTAB. 2',validators=[DataRequired()])
    ESTAB32 = FloatField('ESTAB. 3',validators=[DataRequired()])
    ESTAB42 = FloatField('ESTAB. 4',validators=[DataRequired()])
    carga3 = FloatField('Carga',validators=[DataRequired()])
    ESTAB13 = FloatField('ESTAB. 1',validators=[DataRequired()])
    ESTAB23 = FloatField('ESTAB. 2',validators=[DataRequired()])
    ESTAB33 = FloatField('ESTAB. 3',validators=[DataRequired()])
    ESTAB43 = FloatField('ESTAB. 4',validators=[DataRequired()])
    
    submit = SubmitField('Grabar')


class prueba_carga3(FlaskForm):
    carga_utli_din = FloatField('CARGA UTILIZADA',validators=[DataRequired()])
    peso_carga_din = FloatField('PESO CARGA',validators=[DataRequired()])
    peso_aparejo_din = FloatField('PESO APAREJOS',validators=[DataRequired()])
    long_pluma_din = FloatField('Longitud Pluma',validators=[DataRequired()])
    rad_oper_din = FloatField('Radio de Operación',validators=[DataRequired()])
    ang_pluma_din = FloatField('Angulo de Pluma (°)',validators=[DataRequired()])
    cap_maxima_din = FloatField('Capacidad Máxima',validators=[DataRequired()])
    check1_pru_car = RadioField('Estado de corona (tornamesa)', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check1_pru_car')
    check2_pru_car = RadioField('Sistema movimiento y frenado', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check2_pru_car')
    check3_pru_car = RadioField('Estado de los estabilizadores', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check3_pru_car')
    check4_pru_car = RadioField('Condiciones de estabilidad de la máquina', choices=[('S', 'Satisfactorio'), ('DG', 'Defecto Grave')],default = 'S',render_kw={}, id='check3_pru_car')
    conforme = RadioField('',choices=[('c', 'Conforme'),('nc','No Conforme')],render_kw={}, id='conforme')
        
    submit = SubmitField('Grabar')







class datos_reporte(FlaskForm):
    empresa = StringField('EMPRESA', validators=[DataRequired()],render_kw={"placeholder": "EMPRESA"})
    fec_inpec = DateField('FECHA DE INSPECCIÓN', validators=[DataRequired()],render_kw={"placeholder": "FECHA DE INSPECCIÓN"})
    fec_emision = DateField('FECHA DE EMISIÓN', validators=[DataRequired()],render_kw={"placeholder": "FECHA DE EMISIÓN"})
    fec_expiracion = DateField('FECHA DE EXPIRACIÓN', validators=[DataRequired()],render_kw={"placeholder": "FECHA DE EXPIRACIÓN"})
    lugar_inpec = StringField('LUGAR INSPECCIÓN', validators=[DataRequired()],render_kw={"placeholder": "LUGAR INSPECCIÓN"})
    nom_inspec = StringField('NOMBRE DEL INSPECTOR', validators=[DataRequired()],render_kw={"placeholder": "NOMBRE DEL INSPECTOR"})

    submit = SubmitField('Enviar')


class datos_lmi(FlaskForm):
    empresa = StringField('EMPRESA', validators=[DataRequired()],render_kw={"placeholder": "EMPRESA"})
    num_reporte = StringField('NÚMERO REPORTE', validators=[DataRequired()],render_kw={"placeholder": "NUMERO DE REPORTE"})
    fec_inpec = DateField('FECHA DE INSPECCIÓN', validators=[DataRequired()],render_kw={"placeholder": "FECHA DE INSPECCIÓN"})
    fec_emision = DateField('FECHA DE EMISIÓN', validators=[DataRequired()],render_kw={"placeholder": "FECHA DE EMISIÓN"})
    fec_expiracion = DateField('FECHA DE EXPIRACIÓN', validators=[DataRequired()],render_kw={"placeholder": "FECHA DE EXPIRACIÓN"})
    lugar_inpec = StringField('LUGAR INSPECCIÓN', validators=[DataRequired()],render_kw={"placeholder": "LUGAR INSPECCIÓN"})
    nom_inspec = StringField('NOMBRE DEL INSPECTOR', validators=[DataRequired()],render_kw={"placeholder": "NOMBRE DEL INSPECTOR"})

    submit = SubmitField('Enviar')




class FormChangePassword(FlaskForm):
    password = PasswordField('Password', validators=[Required()])
    submit = SubmitField('Aceptar')


class UploadForm(FlaskForm):
    photo = FileField('selecciona imagen:',validators=[FileRequired()])
    submit = SubmitField('Submit')