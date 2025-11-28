import json

def lambda_handler(event, context):
    """
    AWS Lambda Handler for Google Chat (Python)
    """
    print(f"Received event: {json.dumps(event)}")

    # 1. Parse Event Body
    # API Gateway passes body as a string in 'body' key
    try:
        if 'body' in event:
            chat_event = json.loads(event['body'])
        else:
            chat_event = event
    except Exception as e:
        print(f"Error parsing JSON: {e}")
        return {'statusCode': 400, 'body': 'Invalid JSON'}

    event_type = chat_event.get('chat')
    
    # 2. Define Core Response
    message_content = {}
    
    if event_type.get("addedToSpacePayload"):
        message_content = {'text': "Welcome! I am ready to help."}
    elif event_type.get("removedFromSpacePayload"):
        return
    else:
        message_content = {'text': "Event received."}

    # 3. Apply Wrapper for Add-on Compatibility
    # This specifically addresses "Failed to parse JSON as RenderActions"
    final_response = {
        "hostAppDataAction": {
            "chatDataAction": {
                "createMessageAction": {
                    "message": message_content
                }
            }
        }
    }

    # 4. Return API Gateway Proxy Response
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(final_response)
    }
