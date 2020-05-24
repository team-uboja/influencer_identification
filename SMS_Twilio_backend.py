#created by Steffen Schmidt 5/23/2020

import messaging_handler
from twilio.rest import Client
import system_constants
from flask import Flask, request, redirect, render_template

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def checker():
    print('Website visited')
    return render_template('index.html')

@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    """Send a dynamic reply to an incoming text message"""
    # Get the message the user sent our Twilio number
    backend=SMS_Twilio_backend()
    backend.receiveMessage(request)


if __name__ == "__main__":
    app.run(debug=True)


class SMS_Twilio_backend:


    def sendMessage(self, target_number, message_content):

        client = Client(system_constants.TWILIO_SID, system_constants.TWILIO_TOKEN)

        message = client.messages \
            .create(
                body=message_content,
                from_=system_constants.TWILIO_PHONE_NUMBER,
                #status_callback='http://postb.in/1234abcd',
                to=target_number
            )

        print('New message sent at ' + str(message.date_sent) + ' to ' + str(message.to) + '. Cost: ' + str(message.price) + ' Currency: ' \
              + str(message.price_unit) + ' Content: ' + str(message.body))

        return_values = {}
        return_values['from'] = message.from_
        return_values['to'] = message.to
        return_values['cost'] = message.price
        return_values['currency'] = message.price_unit
        return_values['content'] = message.body
        return_values['created'] = message.date_created
        return_values['sent'] = message.date_sent
        return_values['updated'] = message.date_updated
        return_values['status'] = message.status
        return_values['error_code'] = message.error_code
        return_values['error_message'] = message.error_message

        return return_values


    def receiveMessage(self, request):
        print('Message received: ' + str(request))
        return_values = {}
        return_values['from'] = request.values.get('From', None)
        return_values['to'] = request.values.get('To', None)
        return_values['cost'] = request.values.get('Price', None)
        return_values['currency'] = request.values.get('Price_unit', None)
        return_values['content'] = request.values.get('Body', None)
        return_values['created'] = request.values.get('Date_created', None)
        return_values['sent'] = request.values.get('Date_sent', None)
        return_values['updated'] = request.values.get('Date_updated', None)
        return_values['status'] = request.values.get('Status', None)
        return_values['error_code'] = request.values.get('Error_code', None)
        return_values['error_message'] = request.values.get('Error_message', None)
        return_values['from_city'] = request.values.get('FromCity', None)
        return_values['from_zip'] = request.values.get('FromZip', None)
        handler = messaging_handler.messaging_handler()
        handler.receiveMessage(return_values, request)
