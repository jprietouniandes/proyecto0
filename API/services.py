from flask import Blueprint, render_template, redirect, url_for,  request, flash
from flask_login import login_required, current_user
from .models import User
from .models import Event
from . import db
from .import ma
from datetime import datetime

services = Blueprint('services', __name__)

@services.route('/event/create')
def eventCreate():
    return render_template('create_event.html')

@services.route('/event/created', methods=['POST'])
def eventCreated():

    if not request.form.get('name') or not request.form.get('category') or not request.form.get('place') or not request.form.get('address') or not request.form.get('dateIni') or not request.form.get('dateFinal') or not request.form.get('isVirtual'):
        flash('Campos vacios, ingrese los campos e intente de nuevo')
        return render_template('create_event.html')

    if request.form.get('isVirtual') == 'Presencial':
        isVirtual = False
    else:
        isVirtual = True

    print(request.form)

    newEvent = Event(
            name=request.form.get('name'),
            category=request.form.get('category'),
            place=request.form.get('place'),
            address=request.form.get('address'),
            dateIni=request.form.get('dateIni'),
            dateFinal=request.form.get('dateFinal'),
            creationDate=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), 
            isVirtual=isVirtual,
            user_id=current_user.id
        )

    if newEvent.dateIni > newEvent.dateFinal:
        flash('Fecha de inicio mayor o igual que fecha final')
        return render_template('create_event.html')   

    db.session.add(newEvent)
    db.session.commit()

    events = Event.query.filter_by(user_id=current_user.id).order_by(Event.creationDate.desc()).all()
    return render_template('events.html', events=events)

@services.route('/getevents', methods=['GET'])
def eventsGet():
    events = Event.query.filter_by(user_id=current_user.id).order_by(Event.creationDate.desc()).all() 
    return render_template('events.html', events=events)


@services.route('/getevent/<int:id_event>', methods=['GET'])
def evenGet(id_event):
    event = Event.query.get_or_404(id_event)
    return render_template('show_event.html', event=event)

@services.route('/putevent/<int:id_event>')
def evenPut(id_event):
    event = Event.query.get_or_404(id_event)

    date_time_str = str(event.dateIni)   
    date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
    event.dateIni = str(date_time_obj.date()) + "T" + str(date_time_obj.time())

    date_time_str = str(event.dateFinal)   
    date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
    event.dateFinal = str(date_time_obj.date()) + "T" + str(date_time_obj.time())

    return render_template('edit_event.html', event=event)


@services.route('/deleteevent/<int:id_event>')
def evenDelete(id_event):
    event = Event.query.get_or_404(id_event)
    db.session.delete(event)
    db.session.commit()

    events = Event.query.filter_by(user_id=current_user.id).order_by(Event.creationDate.desc()).all() 
    return render_template('events.html', events=events)
    #return '', 204


@services.route('/event/edited<int:id_event>', methods=['POST'])
def eventEdited(id_event):
    event = Event.query.get_or_404(id_event)

    print(request.form)

    if not request.form.get('name') or not request.form.get('category') or not request.form.get('place') or not request.form.get('address') or not request.form.get('dateIni') or not request.form.get('dateFinal') or not request.form.get('isVirtual'):
        flash('Campos vacios, ingrese los campos e intente de nuevo')
        return render_template('edit_event.html', event=event)

    if 'name' in request.form:
            event.name = request.form.get('name')
    if 'category' in request.form:
            event.category = request.form.get('category')
    if 'place' in request.form:
            event.place = request.form.get('place')
    if 'address' in request.form:
            event.address = request.form.get('address')
    if 'dateIni' in request.form:
            event.dateIni =request.form.get('dateIni')
    if 'dateFinal' in request.form:
            event.dateFinal =request.form.get('dateFinal')
    if 'isVirtual' in request.form:
            if request.form.get('isVirtual') == 'Presencial':
                isVirtual = False
            else:
                isVirtual = True

            event.isVirtual = isVirtual

    if event.dateIni > event.dateFinal:
        flash('Fecha de inicio mayor que fecha final')
        return render_template('edit_event.html', event=event)


    db.session.commit()

    events = Event.query.filter_by(user_id=current_user.id).order_by(Event.creationDate.desc()).all() 
    return render_template('events.html', events=events)



#@services.route('/event/show/<int:event_id>')
#def eventShow(event_id):
 #   event = Event.query.filter_by(id=event_id).first()
  #  return render_template('show_event.html', event=event)
