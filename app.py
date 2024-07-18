from flask import Flask, request, jsonify
import http.client
import json

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello, World!'})



def verificar_token(req):
    token = req.args.get('hub.verify_token')
    challenge = req.args.get('hub.challenge')

    if challenge and token == TOKEN_ANDERCODE:
        return challenge
    else:
        return jsonify({'error':'Token Invalido'}),401

def recibir_mensajes(req):
    try:
        req = request.get_json()
        entry =req['entry'][0]
        changes = entry['changes'][0]
        value = changes['value']
        objeto_mensaje = value['messages']

        if objeto_mensaje:
            messages = objeto_mensaje[0]

            if "type" in messages:
                tipo = messages["type"]


                if tipo == "interactive":
                    tipo_interactivo = messages["interactive"]["type"]

                    if tipo_interactivo == "button_reply":
                        text = messages["interactive"]["button_reply"]["id"]
                        numero = messages["from"]

                        enviar_mensajes_whatsapp(text,numero)
                    
                    elif tipo_interactivo == "list_reply":
                        text = messages["interactive"]["list_reply"]["id"]
                        numero = messages["from"]

                        enviar_mensajes_whatsapp(text,numero)

                if "text" in messages:
                    text = messages["text"]["body"]
                    numero = messages["from"]

                    enviar_mensajes_whatsapp(text,numero)
        
        return jsonify({'message':'EVENT_RECEIVED'})
    except Exception as e:
        return jsonify({'message':'EVENT_RECEIVED'})
    
def enviar_mensajes_whatsapp(texto,number):
    texto = texto.lower()

    if len(number) == 13:
        numero = number[:2]+number[3:]
    else:  
        numero = number
        
    
    if "hola" in texto:
        data={
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": numero,
            "type": "text",
            "text": {
                "preview_url": False,
                "body": f"🚀 Hola, ¿Cómo estás? Bienvenido."
            }
        }
    elif "btnAmperaje" in texto:
                data={
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": numero,
            "type": "text",
            "text": {
                "preview_url": False,
                "body": f"Excelente, para calcular el amperaje necesito que me proporciones la potencia en watts y el voltaje en volts. ¿Podrías proporcionarme esos datos?"
            }
        }
    elif "btnCable" in texto:
                data={
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": numero,
            "type": "text",
            "text": {
                "preview_url": False,
                "body": f"Excelente, El cable es el siguiente"
            }
        }


    
    else:
        data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": numero,
            "type": "interactive",
            "interactive":{
                "type":"button",
                "body": {
                "text": "¿En que puedo ayudarte?"
                },
                "footer": {
                    "text": "Selecciona una de las opciones"
                },
                "action": {
                    "buttons":[
                        {
                            "type": "reply",
                            "reply":{
                                "id":"btnAmperaje",
                                "title":"Calcula Amperaje?"
                            }
                        },{
                            "type": "reply",
                            "reply":{
                                "id":"btnCable",
                                "title":"Que Cable Necesito?"
                            }
                        }
                    ]
                }
            }
        }

    #Convertir el diccionaria a formato JSON
    data=json.dumps(data)
    identificador = "EAAREvz1E5l8BOxY4A5TuRDix5ZBYZBAFZCsMx1SomDm3OTW9DOTxnoNHuUVICFHKaPYy7RKI6I8JXZBZAGBjjVlbfzR1L0Hwb6mta4FwMVMQb9apo11ZAb8bjPTsb76WvqEpabmoaA0GiLTmCfa8PZBWrquRxFUDjkRYoT0YVFLNo3xtTlZCWuZCJg9C6oRgZBRVFpLZBCzvgcBCVjMoKjZA19QZD"
    headers = {
        "Content-Type" : "application/json",
        "Authorization" : f"Bearer {identificador}"
    }

    connection = http.client.HTTPSConnection("graph.facebook.com")

    try:
        connection.request("POST","/v20.0/312280328646454/messages", data, headers)
        response = connection.getresponse()
        print(response.status, response.reason)
    except Exception as e:
        print(e)
    finally:
        connection.close()
    
#Token de verificacion para la configuracion
TOKEN_ANDERCODE = "GARFEXAPP"

@app.route('/webhook', methods=['GET','POST'])
def webhook():
    if request.method == 'GET':
        challenge = verificar_token(request)
        return challenge
    elif request.method == 'POST':
        reponse = recibir_mensajes(request)
        return reponse

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80,debug=True)
