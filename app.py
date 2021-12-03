from flask import Flask, jsonify, json, request
from flask_restful import Resource, Api
from models import Citizens
import requests


app = Flask(__name__)
api = Api(app)

class Citizen(Resource):
    def get(self, cpf):
        person = Citizens.query.filter_by(cpf = cpf).first()

        try:
            response = {
                'surname' : person.surname,
                'name' : person.name,
                'cpf' : person.cpf,
                'phone number' : person.cellphone,
                'cep' : person.cep,
                'neighbourhood' : person.neighbourhood,
                'city' : person.city,
                'email' : person.email
            }

        except Exception as e:
            response = {
                'error' : f'{e}'
            }

        return jsonify(response)

    def put(self, cpf):
        person = Citizens.query.filter_by(cpf = cpf).first()
        data = json.loads(request.data)

        try:
            if 'surname' in data:
                person.surname = data['surname']
            
            if 'email' in data:
                person.email = data['email']

            if 'cellphone' in data:
                person.cellphone = data['cellphone']

            if 'cep' in data:
                person.cep = data['cep']
                address = request.get(f'viacep.com.br/ws/{person.cep}/json/')
                person.street = address.json()['logradouro']
                person.neighbourhood = address.json()['bairro']
                person.city = address.json()['localidade']
                person.state = address.json()['uf']

            person.save()

            response = {
                'success' : 'data updated'
            }

        except Exception as e:
            response = {
                'error' : f'{e}'
            }

        return jsonify(response)


class NewCitizen(Resource):
    def post(self):
        data = json.loads(request.data)
        cep = data['cep']

        try:
            address = requests.get(f'https://viacep.com.br/ws/{cep}/json/')

            # user inserts name, surname, cep, cpf and contacts (phone and email)
            person = Citizens(name = data['name'], surname = data['surname'], cep = data['cep'],
            email = data['email'], cellphone = data['cellphone'], cpf = data['cpf'],
            neighbourhood = address.json()['bairro'], city = address.json()['localidade'],
            state = address.json()['uf'], street = address.json()['logradouro'])

            person.save()

            response = {
                'success' : 'citizen added'
            }

        except Exception as e:
            response = {
                'error' : f'{e}'
            }

        return jsonify(response)

class AllCitizens(Resource):
    def get(self):
        people = Citizens.query.order_by(Citizens.surname)

        try:
            response = [{
                'surname' : person.surname,
                'name' : person.name,
                'cpf' : person.cpf,
                'phone number' : person.cellphone,
                'cep' : person.cep,
                'neighbourhood' : person.neighbourhood,
                'city' : person.city,
                'email' : person.email
            } for person in people]

        except Exception as e:
            response = {
                'error' : f'{e}'
            }

        return jsonify(response)

api.add_resource(Citizen, '/citizen/<string:cpf>')
api.add_resource(NewCitizen, '/add/')
api.add_resource(AllCitizens, '/citizens/')

if __name__ == '__main__':
    app.run(debug = True)