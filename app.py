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
    
    if "hola" in texto:
        data={
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "text",
            "text": {
                "preview_url": False,
                "body": "🚀 Hola, ¿Cómo estás? Bienvenido."
            }
        }
    else:
        data={
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "text",
            "text": {
                "preview_url": False,
                "body": "🚀 Hola, visita mi web anderson-bastidas.com para más información.\n \n📌Por favor, ingresa un número #️⃣ para recibir información.\n \n1️⃣. Información del Curso. ❔\n2️⃣. Ubicación del local. 📍\n3️⃣. Enviar temario en PDF. 📄\n4️⃣. Audio explicando curso. 🎧\n5️⃣. Video de Introducción. ⏯️\n6️⃣. Hablar con AnderCode. 🙋‍♂️\n7️⃣. Horario de Atención. 🕜 \n0️⃣. Regresar al Menú. 🕜"
            }
        }

    #Convertir el diccionaria a formato JSON
    data=json.dumps(data)

    headers = {
        "Content-Type" : "application/json",
        "Authorization" : "Bearer EAAM1QqlQV90BO2QbeOuwedmZAgbAHfCnZBUmQsjP3phs4UEK2fRuYGbZBH7B8nEz3QhV4wt4NEhgfZCvUOQCxZAeNGnaZBBfmMA4ipeMiPD43d2gvxzMrebJm3hilKHcYwOCxZCZCcxJau1wrgugRGehuzs8ZC7jCHzr9lluJvcfUAiYwK5IuQGG7rd4Bz6MoZB902TGkIYdVZBEB1XGzfCOS1HxKccJiv4YLdGcUYZD"
    }

    connection = http.client.HTTPSConnection("graph.facebook.com")

    try:
        connection.request("POST","/v18.0/117721278011867/messages", data, headers)
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
