
 

import os
import json
import requests
import logging
from dotenv import load_dotenv
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

load_dotenv()
logger = logging.getLogger(__name__)

WHATSAPP_TOKEN = 'EAAZAWTB5Dv6MBPAjZAaB677p1jwRhD5nWoXH74zDpeq5cL1mOX2TVywE2KZATan6CZBt8dnubTbe92qTxuIOxLSBtJLmmppP4XqpZAdghnQSjxaX9duFktSRDL4oYDCJPLmTfSdb0Ql4xuvQQehzn9c0DuE98CpkgAvN8ukZADQYd4WpHhqi7e5cvfsjgdFltHtAZDZD'
PHONE_NUMBER_ID = '703676362831088'
WHATSAPP_API_URL = f"https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages"
VERIFY_TOKEN = 'FhfMVzwbdAz3spqkXwB5XcHJxj2ilFgLkaZvEEIv2K5o0qGw7K2HW34GrHoiuc0S'


@csrf_exempt
def send_template_message(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            phone = data.get("phone")  # Format: 31612345678

            payload = {
                "messaging_product": "whatsapp",
                "to": phone,
                "type": "template",
                "template": {
                    "name": "new_job",  
                    "language": { "code": "en_US" },
                    "components": [
                        {
                            "type": "body",
                            "parameters": [
                                {"type": "text", "text": data.get("name", "David")},
                                {"type": "text", "text": data.get("date", "24 July")},
                                {"type": "text", "text": data.get("job_title", "Python Developer")},
                                {"type": "text", "text": data.get("salary", "3000 - 4000")}
                            ]
                        },
                        {
                            "type": "button",
                            "sub_type": "url",
                            "index": "0",  # for the first button
                            "parameters": [
                                {
                                    "type": "text",
                                    "text": "123456789"
                                }
                            ]
                        }
                    ]
                }
            }

            headers = {
                "Authorization": f"Bearer {WHATSAPP_TOKEN}",
                "Content-Type": "application/json"
            }

            response = requests.post(WHATSAPP_API_URL, headers=headers, json=payload)
            return JsonResponse(response.json(), status=response.status_code)

        except Exception as e:
            logger.error(f"Error sending template message: {e}")
            return JsonResponse({"error": "Failed to send message"}, status=500)

    return JsonResponse({"error": "Only POST allowed"}, status=405)


def send_text_message(phone, message):
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "text",
        "text": { "body": message }
    }
    try:
        requests.post(WHATSAPP_API_URL, headers=headers, json=payload)
    except Exception as e:
        logger.error(f"Error sending fallback text message: {e}")


def send_confirmation_template(phone):
    """Send confirmation template when user clicks 'Geen vacatures meer'"""
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "template",
        "template": {
            "name": "confirmation",  # You'll need to create this template in Meta Business Manager
            "language": { "code": "nl_NL" }
        }
    }
    try:
        response = requests.post(WHATSAPP_API_URL, headers=headers, json=payload)
        logger.info(f"Confirmation template sent to {phone}: {response.status_code}")
    except Exception as e:
        logger.error(f"Error sending confirmation template: {e}")


@csrf_exempt
def webhook(request):
    if request.method == "GET":
        mode = request.GET.get("hub.mode")
        token = request.GET.get("hub.verify_token")
        challenge = request.GET.get("hub.challenge")
        if mode == "subscribe" and token == VERIFY_TOKEN:
            return HttpResponse(challenge)
        return HttpResponse("Verification token mismatch", status=403)

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            
            # Handle interactive button responses
            if 'entry' in data and len(data['entry']) > 0:
                changes = data['entry'][0].get('changes', [])
                for change in changes:
                    value = change.get('value', {})
                    
                    # Handle interactive button responses
                    if 'messages' in value:
                        messages = value['messages']
                        for msg in messages:
                            from_number = msg['from']
                            
                            # Handle interactive button responses
                            if msg.get('type') == 'interactive':
                                interactive = msg.get('interactive', {})
                                if interactive.get('type') == 'button_reply':
                                    button_id = interactive['button_reply']['id']
                                    
                                    if button_id == 'geen_vacatures_meer':
                                        # Send confirmation template
                                        send_confirmation_template(from_number)
                                    elif button_id == 'ja_uitschrijven':
                                        # Send unsubscribe confirmation message
                                        reply = "We hebben je uitschrijving ontvangen. Je ontvangt geen vacatures meer.\nBedankt dat je het ons liet weten!"
                                        send_text_message(from_number, reply)
                                    elif button_id == 'nee_doorgaan':
                                        # Send continue message
                                        reply = "Top! We blijven je de beste vacatures sturen.\nVeel succes verder!"
                                        send_text_message(from_number, reply)
                            
                            # Handle text messages (fallback)
                            elif msg.get('type') == 'text':
                                text = msg['text']['body'].strip().lower()
                                
                                if text == "Geen vacatures meer":
                                    send_confirmation_template(from_number)
                                elif text == "Ja, uitschrijven":
                                    reply = "We hebben je uitschrijving ontvangen. Je ontvangt geen vacatures meer.\nBedankt dat je het ons liet weten!"
                                    send_text_message(from_number, reply)
                                elif text == "Nee, doorgaan":
                                    reply = "Top! We blijven je de beste vacatures sturen.\nVeel succes verder!"
                                    send_text_message(from_number, reply)
                                else:
                                    reply = "Hoi!  Je kunt in dit gesprek alleen kiezen uit de knoppen. We kunnen niet reageren op andere berichten. Heb je een vraag? Mail dan naar support@recruitrobin.com. We helpen je daar graag verder."
                                    send_text_message(from_number, reply)
                                    
        except KeyError as e:
            logger.warning(f"No message in webhook payload: {e}")
        except Exception as e:
            logger.error(f"Error handling webhook: {e}")

        return HttpResponse("OK")


