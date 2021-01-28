from .main import main as main_blueprint
from .auth import auth as auth_blueprint
from flask import Flask
from flask import Flask, request
from flask_restful import Api, Resource
from .models import Event
from . import db
from . import ma
from . import api


class User_Schema(ma.Schema):
    class Meta:
        fields = ("id", "email", "password", "events")

user_schema = User_Schema()
users_schema = User_Schema(many = True)

class Event_Schema(ma.Schema):
    class Meta:
        fields = ("id", "name", "category", "place", "address", "dateIni", "dateFinal", "isVirtual", "user_id")

post_schema = Event_Schema()
posts_schema = Event_Schema(many = True)

class EventsGet(Resource):
    def get(self, id_user):
        events = Event.query.filter_by(user_id=id_user).all()
        return posts_schema.dump(events)

class EventsSet(Resource):

    def post(self):
        newEvent = Event(
            name=request.json['name'],
            category=request.json['category'],
            place=request.json['place'],
            address=request.json['address'],
            dateIni=request.json['dateIni'],
            dateFinal=request.json['dateFinal'],
            isVirtual=request.json['isVirtual'],
            user_id=request.json['user_id']#aqui va el ID del usuario desde el front
        )
        db.session.add(newEvent)
        db.session.commit()
        return post_schema.dump(newEvent) 

class EventOne(Resource):

    def get(self, id_event):
        event = Event.query.get_or_404(id_event)
        return post_schema.dump(event)

    def put(self, id_event):
        event = Event.query.get_or_404(id_event)

        if 'name' in request.json:
            event.name = request.json['name']
        if 'category' in request.json:
            event.category = request.json['category']
        if 'place' in request.json:
            event.place = request.json['place']
        if 'address' in request.json:
            event.address = request.json['address']
        if 'dateFinal' in request.json:
            event.dateFinal = request.json['dateFinal']
        if 'isVirtual' in request.json:
            event.isVirtual = request.json['isVirtual']

        db.session.commit()
        return post_schema.dump(event)

    def delete(self, id_event):
        event = Event.query.get_or_404(id_event)
        db.session.delete(event)
        db.session.commit()
        return '', 204 
    
api.add_resource(EventsGet,'/events/<int:id_user>')    
api.add_resource(EventsSet,'/events')
api.add_resource(EventOne,'/events/<int:id_event>')
