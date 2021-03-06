#created by Steffen Schmidt on 5/24/2020
import SMS_Twilio_backend
import system_constants
from flask import Flask, request, redirect, render_template, jsonify, flash, abort, url_for, send_file
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
import csv




#TODO: Fix to relative folder

ALLOWED_EXTENSIONS = {'csv'}


app = Flask(__name__, static_folder= './static')

#initialize Login session handler
login_manager = flask_login.LoginManager(app)
login_manager.session_protection = "strong"
login_manager.login_view = '/login'
app.secret_key = system_constants.SECRET_KEY




app.config['UPLOAD_FOLDER'] = system_constants.UPLOAD_FOLDER

@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def show_main():
    print('main visited')
    print('main test')
    print('By user' + str(flask_login.current_user))
    print('main test2')
    return render_template('index2.html')

@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    """Send a dynamic reply to an incoming text message"""
    # Get the message the user sent our Twilio number
    backend=SMS_Twilio_backend.SMS_Twilio_backend()
    backend.receiveMessage(request)
    return 'True'

#@app.route("/.well-known/pki-validation/F9CB136F4965BB6EEB5E19A2F5B0E807.txt", methods=['GET', 'POST'])
#def activateSSL():
    
#    return render_template('F9CB136F4965BB6EEB5E19A2F5B0E807.txt')

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

@app.route("/processCSV", methods=['GET','POST'])
@flask_login.login_required
def processCSV():
    if request.method=='POST':
        if 'file' in request.files:
            file = request.files['file']

            file_name = werkzeug.utils.secure_filename(file.filename)
            #TODO: abfangen falls files mit gleichem Namen schon existieren
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], system_constants.CSV_FILENAME))
            #handler = messaging_handler.messaging_handler()
            #handler.parseSubmittedCSVFiles()
            #f = open(os.path.join(app.config['UPLOAD_FOLDER'], 'latest_csv.csv'),"w")
            #f.close()
            return True

@app.route("/results", methods=['GET','POST'])
@flask_login.login_required
def show_results():
    tools = analytics_backend.analytics_backend()
    return tools.conductAnalysis()

@app.route("/getFilters", methods=['GET','POST'])
@flask_login.login_required
def get_filters():
    return utils.utils().fillFilters()

@app.route("/getFilteredResultsTable", methods=['GET','POST'])
@flask_login.login_required
def get_filtered_incoming_message_data():
    filter_keys = ['from_', 'from_city', 'campaign_identifier', 'voted_for']
    restriction_dict = {}
    for key in filter_keys:
        restriction_dict[key] = request.args.get(key)
    return jsonify(utils.utils().getSelectedDataIncoming(restriction_dict))

@app.route('/getFilteredResultsBarChart', methods=['GET', 'POST'])
@flask_login.login_required
def getFilteredResultsBarChart():
    filter_keys = ['from_', 'from_city', 'campaign_identifier', 'voted_for']
    restriction_dict = {}
    for key in filter_keys:
        restriction_dict[key] = request.args.get(key)
    return utils.utils().filteredBarChartData(restriction_dict)

#ToDo: anonymize
@app.route('/getFilteredFile', methods=['GET', 'POST'])
@flask_login.login_required
def getFileFiltered():
    print('Called getFileFiltered')
    filter_keys = ['from_', 'from_city', 'campaign_identifier', 'voted_for']
    restriction_dict = {}
    for key in filter_keys:
        restriction_dict[key] = request.args.get(key)
    data_list = utils.utils().getSelectedDataIncoming(restriction_dict)
    f = open("campaign_results.csv", "w")
    f.write("a")
    f.close()
    os.chmod("campaign_results.csv", 0o777)
    with open('campaign_results.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for row in data_list:
            csv_writer.writerow(row)
            print('current row: ' + str(row))

    f = open("campaign_results.csv", "r")
    return_string = f.read()
    return return_string



@app.route('/getFilteredResultsTimeseries', methods=['GET', 'POST'])
@flask_login.login_required
def getFilteredResultsTimeseries():
    filter_keys = ['from_', 'from_city', 'campaign_identifier', 'voted_for']
    restriction_dict = {}
    for key in filter_keys:
        restriction_dict[key] = request.args.get(key)
    return utils.utils().filteredTimeSeriesData(restriction_dict)


@app.route("/dashboard", methods=['GET','POST'])
@flask_login.login_required
def show_dashboard():
    print('Opening dashboard')
    return render_template('dashboard.html')


@app.route('/getaccountdata', methods=['GET','POST'])
@flask_login.login_required
def get_account_data():
    return utils.utils().getUserInfo(flask_login.current_user.get_id())

@app.route('/UpdateProfile', methods=['GET','POST'])
@flask_login.login_required
def update_account_data():

    utils.utils().updateUserInfo(request.args.get('organization'), request.args.get('username'), \
                                 request.args.get('mail'), request.args.get('first_name'), \
                                 request.args.get('last_name'), request.args.get('city'), \
                                 request.args.get('country'))
    return redirect(url_for('show_account_info'))

@app.route('/LaunchCampaign', methods=['GET','POST'])
@flask_login.login_required
def launch_campaign():
    print('launch campaign')
    print(request.args)
    utils.utils().writeCampaignInfo(request.args.get('organization'), request.args.get('username'), \
                                 request.args.get('mail'), request.args.get('geography'), \
                                 request.args.get('collaborators'), request.args.get('description'),request.args.get('campaign_identifier'))
    print('Message array: ' + str(request.args.getlist('message_array[0][]')))
    messaging_handler.messaging_handler().sendOutMessages(request.args.getlist('message_array[0][]'), request.args.get('campaign_identifier'))
    print('here')
    return redirect(url_for('show_success'))

@app.route('/privacy_policy', methods=['GET','POST'])
def show_privacy_policy():
    return render_template('privacy-policy.html')

@app.route('/cookie_policy', methods=['GET','POST'])
def show_cookie_policy():
    return render_template('cookie-policy.html')

@app.route('/LaunchInfoCampaign', methods=['GET','POST'])
@flask_login.login_required
def launch_info_campaign():
    print('launch campaign')
    print(request.args)
    messaging_handler.messaging_handler().sendOutInfoMessages(request.args.getlist('message_array[]'), request.args.get('campaign_identifier'),request.args.get('message'))
    print('here')
    #this is a horrible hack, should redirect to 'show_success' but that does not work for some reason
    return render_template('success.html')

@app.route("/success", methods=['GET','POST'])
@flask_login.login_required
def show_success():
    print('success')
    return render_template('success.html')


@app.route("/join", methods=['GET','POST'])
def show_join():
    print('Rendering "join the team" page')
    return render_template('join.html')


@app.route("/account", methods=['GET','POST'])
@flask_login.login_required
def show_account_info():
    print('Opening Account')
    return render_template('account.html')

@app.route("/newcampaign", methods=['GET','POST'])
@flask_login.login_required
def show_new_campaign_page():
    print('Opening New Campaign Page')
    return render_template('newcampaign.html')

@app.route("/outgoing", methods=['GET','POST'])
@flask_login.login_required
def show_new_outgoing_campaign_page():
    print('Opening New Outgoing Campaign Page')
    return render_template('newoutgoing.html')


@app.route('/checkloginstatus', methods=['GET', 'POST'])
def checkloginstatus():
    print('check log-in status')
    if flask_login.current_user.is_authenticated == True:
        return {'login_status': 1}

    return {'login_status': 0}


@app.route('/logout', methods=['GET', 'POST'])
@flask_login.login_required
def logout():
    flask_login.logout_user()

    return redirect(url_for('show_main'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask_login.current_user.is_authenticated:
        return redirect(url_for('show_main'))
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
            print(flask_login.login_user(User.User(username)))
            print('Login done')
            if str(request.referrer).split("=%2F").__len__() >= 2:
                next = '/' + str(request.referrer).split("=%2F")[1]
            else:
                next = None
            print('Next read')
            print(next)
            print(request)
            print('Current user: ' + str(flask_login.current_user))
            # is_safe_url should check if the url is safe for redirects.
            # See http://flask.pocoo.org/snippets/62/ for an example.
            #if not is_safe_url.is_safe_url(next,{'identifylocalinfluencers.com'}):
            #    return abort(400)
            if next == None:
                return redirect(url_for('show_main'))
            return redirect(next)
        else:
            render_template('login.html', form=form, success_label = "False username or password")
    return render_template('login.html', form=form)


#login handling

@login_manager.user_loader
def load_user(user_id):
    print('User id to load: ' + str(user_id))
    myutils = utils.utils()
    user_data = myutils.readFromUserDB(user_id)
    user = User.User(user_data['username'])
    return user


if __name__ == "__main__":
    app.run(debug=True)