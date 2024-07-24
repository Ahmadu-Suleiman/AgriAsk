from flask import Flask, request, render_template_string, redirect, url_for, Response

from sendSMS import send_sms

app = Flask(__name__)

# Simulate a database
tech_events = []  # Events in the database
users = ["+2348138445664", "+2348027020206"]  # User phone numbers in the database


@app.route('/', methods=['GET'])
def index():
    return render_template_string('''  <style>
            form{
                font-family: sans-serif;
                left: 50%;
                position: absolute;
                top: 50%;
                transform: translate(-50%,-50%);
                max-width: 300px;
                width: 100%;
            }
            h1{
                margin-bottom: 1rem;
                color: steelblue;
            }
            input, textarea{
                border: 1px solid silver;
                border-radius: 5px;
                padding: .5rem 1rem;
                width: 100%;
            }
        </style>
          <form action="/event" method="post">
            <h1>Add Event</h1>
            <label for="name">Name:</label><br>
            <input type="text" id="name" name="name"><br><br>
            <label for="msg">Description:</label><br>
            <textarea type="text" id="description" name="description"rows="4"></textarea><br><br>
            <label for="date">Date:</label><br>
            <input type="date" id="date" name="date"><br><br>
            <input type="submit">
          </form>''')


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
    app.run(host='0.0.0.0', port=3000)
