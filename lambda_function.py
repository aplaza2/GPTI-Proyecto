import json
import boto3

def lambda_handler(event, context):
    
    # Obtener el tipo de intent y los sessionAttributes
    intent_name = event['request']['intent']['name']
    session_attributes = event['session'].get('attributes', {})
    
    if intent_name == 'RegisterUserIntent':
        # Primera interacción: pedir el nombre
        return ask_for_name()

    elif intent_name == 'CaptureNameIntent':
        # Capturamos el nombre y guardamos en sessionAttributes
        name = event['request']['intent']['slots']['name']['value']
        session_attributes['name'] = name
        return ask_for_age(session_attributes)
    
    elif intent_name == 'CaptureAgeIntent':
        # Capturamos la edad y damos la bienvenida
        age = event['request']['intent']['slots']['age']['value']
        name = session_attributes.get('name')
        
        # Guardar los datos en la base de datos
        save_user_data(name, age)
        
        # Mensaje de bienvenida
        return welcome_user(name, age)
    
def ask_for_name():
    return {
        'version': '1.0',
        'sessionAttributes': {},
        'response': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': 'Claro, ¿cuál es tu nombre?'
            },
            'shouldEndSession': False
        }
    }

def ask_for_age(session_attributes):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': '¿Cuál es tu edad?'
            },
            'shouldEndSession': False
        }
    }

def welcome_user(name, age):
    return {
        'version': '1.0',
        'sessionAttributes': {},
        'response': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': f'Bienvenido {name} de {age} años.'
            },
            'shouldEndSession': True
        }
    }

def save_user_data(name, age):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Users')
    table.put_item(
        Item={
            'name': name,
            'age': int(age)
        }
    )
