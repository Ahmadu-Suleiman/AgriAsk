from flask import Flask, request, redirect, url_for, Response, render_template

from sendSMS import send_sms

app = Flask(__name__)

# Simulate a database
tech_events = []  # Events in the database
users = ["+2348138445664", "+2348027020206"]  # User phone numbers in the database


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/event', methods=['POST'])
def add_event():
    form_data = request.form
    if not form_data['name'] or not form_data['description'] or not form_data['date']:
        send_sms(form_data['from'], "Please provide all the required information.")
        return "Bad Request", 400

    event_id = len(tech_events) + 1
    tech_events.append({
        'id': event_id,
        'name': form_data['name'],
        'description': form_data['description'],
        'date': form_data['date'],
    })

    send_sms(users, f"Event Id: {event_id}\n{form_data['description']}")  # Broadcast the created Event to all users
    return redirect(url_for('index'))


@app.route('/incoming-messages', methods=['POST'])
def handle_incoming_messages():
    form_data = request.form
    print(form_data)
    event_id = form_data['text']
    event_sender = form_data['from']
    print('from: ', event_sender)
    event = next((e for e in tech_events if str(e['id']) == event_id), None)

    if not event:
        send_sms(to_numbers=event_sender, message=f"{event_id} not valid. Please provide a valid event Id.")
        return Response(status=200)

    send_sms(to_numbers=event_sender, message=f"You have saved a spot at {event['name']}")
    return Response(status=200)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
