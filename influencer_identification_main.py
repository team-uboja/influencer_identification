#created by Steffen Schmidt on 5/24/2020
import SMS_Twilio_backend
import system_constants
from flask import Flask, request, redirect, render_template, jsonify, flash, abort, url_for
import os
import messaging_handler
import werkzeug.utils
import analytics_backend
import flask_login
import utils
import User
import wtforms
import Forms
import is_safe_url



#TODO: Fix to relative folder

ALLOWED_EXTENSIONS = {'csv'}


app = Flask(__name__, static_folder= './static')

#initialize Login session handler
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"
login_manager.login_view = '/login'
app.secret_key = system_constants.SECRET_KEY


app.config['UPLOAD_FOLDER'] = system_constants.UPLOAD_FOLDER

@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def show_main():
    print('Website visited')
    return render_template('index.html')

@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    """Send a dynamic reply to an incoming text message"""
    # Get the message the user sent our Twilio number
    backend=SMS_Twilio_backend.SMS_Twilio_backend()
    backend.receiveMessage(request)

@app.route("/demo", methods=['GET','POST'])
@flask_login.login_required
def show_demo():
    req = request.form
    print(req)
    
    if request.method=='POST':
        if 'file' in request.files:
            file = request.files['file']

            file_name = werkzeug.utils.secure_filename(file.filename)
            #TODO: abfangen falls files mit gleichem Namen schon existieren
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], system_constants.CSV_FILENAME))
            handler = messaging_handler.messaging_handler()
            handler.parseSubmittedCSVFiles()
            #f = open(os.path.join(app.config['UPLOAD_FOLDER'], 'latest_csv.csv'),"w")
            #f.close()
            return render_template('demo.html', success_label = "Messages sent!")

        
    return render_template('demo.html')


@app.route("/checkpassword", methods=['GET','POST'])
def check_password():
    if 'password' in request.args:
        password = request.args.get('password')
        if (password == "TEAMUBOJA2020"):
            print ("Demo access succeeded")
            return jsonify({"success":True})


@app.route("/results", methods=['GET','POST'])
def show_results():
    tools = analytics_backend.analytics_backend()
    return tools.conductAnalysis()

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = Forms.LoginForm(request.form)
    print(form)
    print(form.validate())
    if form.validate():
        # Login and validate the user.
        # user should be an instance of your `User` class
        myutils = utils.utils()
        username = str(form.username.data).split(',')[0]
        password = str(form.password.data).split(',')[0]

        if myutils.check_password(username, password):

            print('Login initiated')
            flask_login.login_user(User.User(username))
            print('Login done')



            next = request.args.get('next')
            print('Next read')
            print(next)
            # is_safe_url should check if the url is safe for redirects.
            # See http://flask.pocoo.org/snippets/62/ for an example.
            #if not is_safe_url.is_safe_url(next,{'identifylocalinfluencers.com'}):
            #    return abort(400)

            return redirect(next)
    return render_template('login.html', form=form)


#login handling

@login_manager.user_loader
def load_user(user_id):
    myutils = utils.utils()
    user_data = myutils.readFromUserDB(user_id)
    user = User.User(user_data['username'], user_data['mail'])
    return user



if __name__ == "__main__":
    app.run(debug=True)