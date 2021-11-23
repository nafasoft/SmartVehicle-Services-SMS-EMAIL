#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 19 14:53:43 2021

@author: juansebastiangambajacomussi
"""

import os
from flask import Flask
from twilio.rest import Client
from flask import request
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = Flask(__name__)

@app.route("/send-sms")
def enviar_sms():
    try:
        # Find your Account SID and Auth Token at twilio.com/console
        # and set the environment variables. See http://twil.io/secure
        account_sid = os.environ['TWILIO_ACCOUNT_SID']
        auth_token = os.environ['TWILIO_AUTH_TOKEN']
        client = Client(account_sid, auth_token)
        contenido= request.args.get("mensaje")
        destino= request.args.get("telefono")
        message = client.messages \
                        .create(
                             body=contenido,
                             from_='+16622004794',
                             to= '+57' + destino
                         )
        
        print(message.sid)
        return 'Enviado correctamente'
    
    except Exception as e:
        return 'Error enviando el mensaje'    

@app.route("/send-email")
def enviar_email():
    # using SendGrid's Python Library
    # https://github.com/sendgrid/sendgrid-python
    destino = request.args.get("correo_destino")
    asunto = request.args.get("asunto")
    mensaje = request.args.get("contenido")
    
    
    message = Mail(
        from_email='sebastiangamba.music@gmail.com',
        to_emails=destino,
        subject=asunto,
        html_content=mensaje)
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
        return 'Email enviado correctamente'
    except Exception as e:
        print(e.message)
        return 'Error enviando el email'
    
if __name__ == '__main__':
    app.run()
