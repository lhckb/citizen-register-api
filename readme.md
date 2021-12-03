# Citizen Register API

### AS OF DECEMBER 3rd, 2021, I HAVE STARTED DEVELOPMENT OF THIS PROJECT THIS MORNING, WILL BE TESTING MORE AND DEBUGGING ON THE NEXT FEW DAYS

This API was developed in Flask using Flask-Restful in Python 3.9.5 

It can Create, Read, Update and Delete information.
It will also communicate with the ViaCEP API to get adresses based on the CEP
obs.: CEP is the Brazilian postal code.

How to use it:
1. first you need to install packges and dependencies using `pip install` on your terminal. requirements can be found on requirements.txt file.
2. second step is to run models.py to create the database, or else the main application won't function.
3. now you can start running app.py and use your prefered way to communicate with it. i used Postman during development.
obs.: you can use playground.py to manipulate data directly from your terminal.

Now please mind for the JSON formatting on moving data:

    for the "/citizen/string:cpf" route:
    1. put method -
        {
            "<desired info to change>" : "<data>"
        }
        on this put method you can alter email, cep, cellphone and surname.

    2. get and delete method -
        all you have to do is pass the CPF through the route

    
    for the "/add/" route:
    1. post method-
        {
            "name" : "john",
            "surname" : "doe",
            "cpf" : "12345678912",
            "cep" : "55123000",
            "email" : "john-doe@gmail.com",
            "cellphone" : "912345678"
        }
        given the CEP number, the rest of the address will be filled using ViaCEP

    
    for the "/citizens/" route:
    1. get method-
        no need to pass anything, this route is for querying every person on the database.