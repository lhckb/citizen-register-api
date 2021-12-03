import requests
from models import Citizens

def insertNew():
    name = input('name: ')
    surname = input('surname: ')
    cpf = input('CPF (numbers only): ')
    cellphone = input('cellphone (numbers only): ')
    email = input('email (can leave empty): ')
    cep = input('CEP (numbers only): ')

    address = requests.get(f'https://viacep.com.br/ws/{cep}/json/')

    newCitizen = Citizens(name = name, surname = surname, cpf = cpf,
    cellphone = cellphone, email = email, cep = cep, neighbourhood = address.json()['bairro'],
    city = address.json()['localidade'], state = address.json()['uf'], street = address.json()['logradouro'])

    newCitizen.save()

def update():
    cpf = input('cpf of citizen: ')
    person = Citizens.query.filter_by(cpf = cpf).first()
    choice = ''

    while choice != '5':
        choice = input('''what info do you want to change? 1- surname, 2- email,
        3- cellphone, 4- cep, 5- exit: ''')

        if choice == '1':
            newSurname = input('new surname: ')
            person.surname = newSurname
            person.save()

        elif choice == '2':
            newEmail = input('new email: ')
            person.email = newEmail
            person.save()

        elif choice == '3':
            newCellphone = input('new cellphone (numbers only): ')
            person.cellphone = newCellphone
            person.save()

        elif choice == '4':
            newCep = input('new CEP (numbers only): ')
            address = requests.get(f'https://viacep.com.br/ws/{newCep}/json/')

            person.cep = newCep
            person.city = address.json()['localidade']
            person.street = address.json()['logradouro']
            person.state = address.json()['uf']
            person.neighbourhood = address.json()['bairro']

            person.save()

        elif choice == '5':
            print('back to main loop\n')

        else:
            print('invalid choice')
            continue


def queryAll():
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

    print(response)

def queryByCPF():
    cpf2query = input('CPF (numbers only) of person to query: ')
    person = Citizens.query.filter_by(cpf = cpf2query).first()
    print(person)

def delete():
    cpf2delete = input('CPF of person to be deleted (numbers only): ')
    remove = requests.delete(f'http://127.0.0.1:5000/citizen/{cpf2delete}')

choice = ''
while choice != '6':
    choice = input('''1- insert new citizen; 2- update info on citizen; 3- query all;
    4- query specific; 5- delete specific; 6- exit: ''')

    if choice == '1':
        insertNew()

    elif choice == '2':
        update()

    elif choice == '3':
        queryAll()

    elif choice == '4':
        queryByCPF()

    elif choice == '5':
        delete()

    elif choice == '6':
        print('program stopped')

    else:
        print('invalid choice')
        continue
