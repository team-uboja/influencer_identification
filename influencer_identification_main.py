#created by Steffen Schmidt on 5/24/2020
import SMS_Twilio_backend
import system_constants
from flask import Flask, request, redirect, render_template

import werkzeug.utils as utils

app = Flask(__name__, static_folder= './static')

@app.route("/", methods=['GET', 'POST'])
def show_main():
    print('Website visited')
    return render_template('index_new.html')

@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    """Send a dynamic reply to an incoming text message"""
    # Get the message the user sent our Twilio number
    backend=SMS_Twilio_backend.SMS_Twilio_backend()
    backend.receiveMessage(request)

@app.route("/demo", methods=['GET','POST'])
def show_demo():
    if request.method=='POST':
        for file in request.files:
            file_name = utils.secure_filename(file.filename)

    return render_template('demo.html')



if __name__ == "__main__":
    app.run(debug=True)