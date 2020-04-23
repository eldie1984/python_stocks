# Forms for admin blueprint
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,IntegerField,FloatField,DateField,SelectField,BooleanField
from wtforms.validators import DataRequired,Optional
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from ..models import Alyc

class BoletosForm(FlaskForm):
    """
    Form for admin to add or edit a department
    """
    numero = IntegerField('Numero', validators=[DataRequired()])
    fecha_concertacion = DateField('Fecha Concertacion',format='%d/%m/%Y')
    fecha_liquidacion=DateField('Fecha Liquidacion',format='%d/%m/%Y')
    cantidad=IntegerField('Cantidad', validators=[DataRequired()])
    tipo_operacion=SelectField('Tipo Operacion', choices=[('cc', 'Compra Contado'),('vc','Venta Contado'),('acc', 'Apertura Colocadora Contado'), ('acf', 'Apertura Colocadora Futuro'),('ocl','Opción Compra Lanzador (Call Venta)'),('atc','Apertura Tomadora Contado (Tipo Caución)'),('atf','Apertura Tomadora Futuro (Tipo Caución)'),('lc','Licitación Compra')])
    tiker=StringField('Ticker', validators=[DataRequired()])
    arancel=FloatField('Arancel', validators=[DataRequired()])
    perc_arancel=FloatField('Porcentaje', validators=[DataRequired()])
    mercado_importe=FloatField('Mercado Importe', validators=[DataRequired()])
    iva=BooleanField('Iva')
    #precio_promedio=FloatField('Comitente', validators=[DataRequired()])
    bruto=FloatField('Bruto', validators=[DataRequired()])
    neto=FloatField('Neto', validators=[DataRequired()])
    moneda=SelectField(u'Moneda', choices=[('p', 'Pesos'), ('d', 'Dolar')],default='p')
    tipo_cambio=FloatField('Tipo Cambio', default=1)
    tipo_cambio_arancel=FloatField('Tipo Cambio Arancel', default=1)
    interes=FloatField('Interes')
    alyc_id=QuerySelectField(query_factory=lambda: Alyc.query.all(),
                                  get_label="name")
    submit = SubmitField('Submit')


class TickerForm(FlaskForm):
    """
    Form for admin to add or edit a department
    """
    boleto_id=IntegerField('Boleto Nro', validators=[DataRequired()],render_kw={'readonly': True})
    date=DateField('Fecha',format='%d/%m/%Y',render_kw={'readonly': True})
    type=SelectField('Tipo', choices=[('cc', 'Compra'), ('vc', 'Venta')],render_kw={'readonly': True})
    tiker=StringField('Ticker', validators=[DataRequired()],render_kw={'readonly': True})
    quantity=IntegerField('Cantidad', validators=[DataRequired()])
    price=FloatField('Precio', validators=[DataRequired()])
    submit = SubmitField('Submit')
