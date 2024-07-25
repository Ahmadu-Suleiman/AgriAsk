from flask import Flask, request, redirect, url_for, Response, render_template

import firebase
from gemini import get_response
from sendSMS import send_sms

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/error')
def error():
    return render_template('error.html')


@app.route('/add-member', methods=['POST'])
def add_member():
    form_data = request.form
    name = form_data['name']
    number = form_data['number']
    if not name or not number:
        return redirect(url_for('error'))

    number = number.replace(' ', '')
    firebase.add_member(name=name, number=number)
    send_sms(number, f'''
        Welcome to AgriAsk, {name}. Ready to answer your farming questions. 
        What would you like to know today?''')
    return redirect(url_for('index'))


@app.route('/incoming-messages', methods=['POST'])
def handle_incoming_messages():
    form_data = request.form
    print(form_data)
    prompt = form_data['text']
    sender = form_data['from']

    response = get_response(prompt=prompt, number=sender)
    send_sms(sender, response)
    return Response(status=200)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
