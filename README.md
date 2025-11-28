📘 Explicación del código (AWS Lambda para Google Chat)

Este código implementa una función AWS Lambda diseñada para recibir eventos desde Google Chat mediante API Gateway y responder en el formato correcto que exige la API de Google Chat Add-ons.

La función procesa mensajes entrantes, detecta eventos como cuando la app es añadida o removida de un espacio, y envía un mensaje estructurado bajo el wrapper requerido por Google Chat (hostAppDataAction → chatDataAction → createMessageAction).

🔍 1. Recepción del evento y parsing del JSON

Cuando Google Chat envía un evento a la Lambda a través de API Gateway, este llega en el campo event['body'] como un string JSON.
El código verifica si el evento viene encapsulado o no, y luego lo convierte en un diccionario de Python:

if 'body' in event:
    chat_event = json.loads(event['body'])
else:
    chat_event = event


Esto permite compatibilidad tanto para pruebas locales como para invocaciones reales desde API Gateway.

En caso de error al procesar el JSON, se devuelve un HTTP 400:

return {'statusCode': 400, 'body': 'Invalid JSON'}

🔎 2. Identificación del tipo de evento

Google Chat envía diferentes tipos de eventos dentro del campo chat.

El código evalúa si:

La app fue añadida a un espacio (addedToSpacePayload)

Fue removida del espacio (removedFromSpacePayload)

O si simplemente recibió un mensaje u otro evento

event_type = chat_event.get('chat')


Dependiendo del evento, se define el contenido del mensaje:

if event_type.get("addedToSpacePayload"):
    message_content = {'text': "Welcome! I am ready to help."}
elif event_type.get("removedFromSpacePayload"):
    return
else:
    message_content = {'text': "Event received."}

🎁 3. Construcción del formato de respuesta para Google Chat

Google Chat (en su modo "Add-on") requiere un formato específico para entregar mensajes desde una app.
Si no se envía en el wrapper adecuado, aparece el error:

"Failed to parse JSON as RenderActions"

El código aplica la estructura necesaria:

final_response = {
    "hostAppDataAction": {
        "chatDataAction": {
            "createMessageAction": {
                "message": message_content
            }
        }
    }
}


Este wrapper es fundamental para que Google Chat procese correctamente la respuesta.

📤 4. Respuesta para API Gateway

Finalmente, la Lambda devuelve un objeto compatible con Proxy Integration de API Gateway:

return {
    'statusCode': 200,
    'headers': {'Content-Type': 'application/json'},
    'body': json.dumps(final_response)
}


Esto completa el flujo:
Google Chat → API Gateway → Lambda → API Gateway → Google Chat.

✅ Resumen

Esta Lambda:

Recibe mensajes y eventos desde Google Chat.

Valida y procesa el JSON entrante.

Reconoce eventos clave (add/remove/message).

Construye y devuelve un mensaje en el formato correcto para Google Chat Add-ons.

Funciona a través de API Gateway con proxy integration (HTTPS requerido).
