# Views for boletos blueprint
from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from sqlalchemy import func

from . import boletos
from .forms import BoletosForm,TickerForm
from .. import db
from ..models import Boleto,Share,Movement,Portfolio

# Boleto Views


@boletos.route('/boletos', methods=['GET', 'POST'])
@login_required
def list_boletos():
    """
    List all boletos
    """


    boletos = Boleto.query.all()

    return render_template('boletos/boletos.html',
                           boletos=boletos, title="Boletos")


@boletos.route('/boletos/add', methods=['GET', 'POST'])
@login_required
def add_boleto():
    """
    Add a boletos to the database
    """


    add_boleto = True

    form = BoletosForm()
    if form.validate_on_submit():

        boleto = Boleto(numero = form.numero.data,
                        fecha_concertacion = form.fecha_concertacion.data,
                        fecha_liquidacion=form.fecha_liquidacion.data,
                        tipo_operacion=form.tipo_operacion.data,
                        tiker=form.tiker.data,
                        cantidad=form.cantidad.data,
                        bruto=form.bruto.data,
                        arancel=form.arancel.data,
                        perc_arancel=form.perc_arancel.data,
                        mercado_importe=form.mercado_importe.data,
                        neto=form.neto.data,
                        iva=form.iva.data,
                        moneda=form.moneda.data,
                        tipo_cambio=form.tipo_cambio.data,
                        tipo_cambio_arancel=form.tipo_cambio_arancel.data,
                        alyc_id=form.alyc_id.data.id)
        if  form.tipo_operacion.data=='vc':
            movement=Movement(boleto_nro=boleto.numero,
            fecha=boleto.fecha_concertacion,
            tipo_operacion=boleto.tipo_operacion,
            monto=boleto.neto,
            tipo_cambio=boleto.tipo_cambio,
            alyc_id=boleto.alyc_id)
        elif  form.tipo_operacion.data=='cc':
            movement=Movement(boleto_nro=boleto.numero,
            fecha=boleto.fecha_concertacion,
            tipo_operacion=boleto.tipo_operacion,
            monto=-boleto.neto,
            tipo_cambio=boleto.tipo_cambio,
            alyc_id=boleto.alyc_id)
        try:
            # add boleto to the database
            db.session.add(boleto)
            db.session.add(movement)
            db.session.commit()
            flash('You have successfully added a new boleto.')
        except Exception as e:
            # in case boleto name already exists
            flash(str(e))

        # redirect to boletos page
        return redirect(url_for('boletos.add_ticker', boleto_id=boleto.id))

    # load boleto template
    return render_template('boletos/boleto.html', action="Add",
                           add_boleto=add_boleto, form=form,
                           title="Add Boleto")


@boletos.route('/boletos/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_boleto(id):
    """
    Edit a boletos
    """


    add_boleto = False

    boleto = Boleto.query.get_or_404(id)
    form = BoletoForm(obj=boleto)
    if form.validate_on_submit():
        boleto.name = form.name.data
        boleto.contraparte = form.contraparte.data
        boleto.commitent = form.commitent.data
        db.session.commit()
        flash('You have successfully edited the boleto.')

        # redirect to the boletos page
        return redirect(url_for('boletos.list_boletos'))

    form.contraparte.data = boleto.contraparte
    form.commitent.data = boleto.commitent
    form.name.data = boleto.name
    return render_template('boletos/boleto.html', action="Edit",
                           add_boleto=add_boleto, form=form,
                           boleto=boleto, title="Edit boleto")


@boletos.route('/boletos/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_boleto(id):
    """
    Delete a boleto from the database
    """


    boleto = Boleto.query.get_or_404(id)
    db.session.delete(boleto)
    db.session.commit()
    flash('You have successfully deleted the boleto.')

    # redirect to the boletos page
    return redirect(url_for('boletos.list_boletos'))

    return render_template(title="Delete Boleto")

@boletos.route('/boletos/accion/add/<boleto_id>', methods=['GET', 'POST'])
@login_required
def add_ticker(boleto_id):
    """
    Add a ticker to the database
    """


    add_ticker = True
    boleto = Boleto.query.get_or_404(boleto_id)
    form = TickerForm()
    cantidad=boleto.cantidad
    if form.validate_on_submit():
        ticker = Share(tiker=form.tiker.data,
                                type=form.type.data,
                                quantity=form.quantity.data,
                                price = form.price.data,
                                date = form.date.data,
                                boleto_id = form.boleto_id.data,
                                dolar = 0)
        if form.type.data =='vc':
            portfolio=Portfolio.query.filter_by(ticker=form.tiker.data).first()
            portfolio.quantity=portfolio.quantity-form.quantity.data
        else:
            try:
                portfolio=Portfolio.query.filter_by(ticker=form.tiker.data).first()
                portfolio.quantity=portfolio.quantity+form.quantity.data
            except:
                portfolio=Portfolio(ticker=form.tiker.data,quantity=form.quantity.data,dolar=form.dolar.data)
        try:
            # add boleto to the database
            db.session.add(ticker)
            db.session.add(portfolio)
            db.session.commit()
            flash('You have successfully added a new boleto.')
        except Exception as e:
            # in case boleto name already exists
            flash(str(e))
        print(cantidad)
        if cantidad != form.quantity.data:
            cantidad=cantidad - form.quantity.data
            form.price.data=0
            form.quantity.data=cantidad
            return render_template('boletos/ticker.html', action="Add",
                                   add_boleto=add_ticker, form=form,
                                   title="Add other Boleto")
        else:
            return render_template('boletos/boleto.html', action="Edit",
                               add_boleto=add_boleto, form=form,
                               boleto=boleto, title="Edit boleto")
        # redirect to boletos page
        return redirect(url_for('boletos.add_ticker'))

    form.date.data = boleto.fecha_liquidacion
    form.tiker.data = boleto.tiker
    form.boleto_id.data = boleto.numero
    form.type.data = boleto.tipo_operacion
    # load boleto template
    return render_template('boletos/ticker.html', action="Add",
                           add_boleto=add_ticker, form=form,
                           title="Add Boleto")
