import os # Modulo utile per la gestione delle variabili d'ambiente

import boto3 # SDK di Lambda per Python
from flask import Flask, jsonify, make_response, request

app = Flask(__name__)

# Creo un oggetto per DynamoDB in modalità client (non in modalità resource)
dynamodb_client = boto3.client('dynamodb')


# Recupero il nome della tabella da una variabile d'ambiente USERS_TABLE defiinita in serverless.yml
USERS_TABLE = os.environ['USERS_TABLE'] 


# Definisco la rotta getUserById su Flask
@app.route('/getUserById/<string:user_id>')
def get_user(user_id):
    result = dynamodb_client.get_item(
        TableName=USERS_TABLE, Key={'userId': {'S': user_id}}
    ) # Recupero l'elemento dalla tabella DynamoDB
    
    item = result.get('Item')
    if not item:
        # Se l'elemento non esiste, ritorno un errore 404 con un messaggio JSON
        return jsonify({'error': 'Could not find user with provided "userId"'}), 404

    # Ritorno l'elemento trovato in formato JSON
    return jsonify(
        {'userId': item.get('userId').get('S'), 'name': item.get('name').get('S')}
    )


# Definisco la rotta createUser su Flask
@app.route('/createUser', methods=['POST'])
def create_user():
    # Recupero i dati inviati nella richiesta POST decodificando il body JSON della richiesta
    user_id = request.json.get('userId')
    name = request.json.get('name')
    
    if not user_id or not name:
        # Se manca uno dei due campi, ritorno un errore 400 con un messaggio JSON
        return jsonify({'error': 'Please provide both "userId" and "name"'}), 400
    
    result = dynamodb_client.get_item(
        TableName=USERS_TABLE, Key={'userId': {'S': user_id}}
    ) # Recupero l'elemento dalla tabella DynamoDB
    
    item = result.get('Item')
    if not item:
        # Inserisco l'elemento nella tabella DynamoDB
        dynamodb_client.put_item(
            TableName=USERS_TABLE, Item={'userId': {'S': user_id}, 'name': {'S': name}}
        )

        # Ritorno i dati inseriti in formato JSON
        return jsonify({'userId': user_id, 'name': name})
    else:
        # Se l'elemento esiste già, ritorno un errore 409 con un messaggio JSON
        return jsonify({'error': 'User with provided "userId" already exists'}), 409


# Definisco ll'handler per l'errore 404 di una rotta non trovata
@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)
