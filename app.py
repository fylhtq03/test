from flask import Flask, render_template, request
from yookassa import Configuration, Payment
import uuid
import requests

podpislon_api_key = 'your_api_key'
Configuration.account_id = 'shop_id'
Configuration.secret_key = 'Секретный ключ'

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])
def data_input():
  if request.method == 'POST':
    global name, second_name, last_name, number
    name = request.form['name']
    second_name = request.form['second_name']
    last_name = request.form['last_name']
    number = request.form['number']
    print(name)
    print(second_name)
    print(last_name)
    print(number)
    #podpislon_create_doc_send()
    Pay_create()
    return render_template('index.html')

def podpislon_create_doc_send():
    headers = {
        'X-Api-Key': podpislon_api_key,
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }

    json_data = {
        'name': name,
        'second_name': second_name,
        'last_name': last_name,
        'phone': number,
        'agreement': 'Y',
        'contacts': [
            [
                {
                    'name': name,
                    'second_name': second_name,
                    'last_name': last_name,
                    'phone': number,
                },
            ],
        ],
    }

    response = requests.put('https://podpislon.ru/integration/add-document', headers=headers, json=json_data)
    print(response)

def Pay_create():
    idempotence_key = str(uuid.uuid4())
    print("idempotence_key:" + idempotence_key)
    payment_data = {
        "id": idempotence_key,
        "status": "pending",
        "paid": "false",
        "amount": {
            "value": "100.00",
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "confirmation_url": "https://yoomoney.ru/api-pages/v2/payment-confirm/epl?orderId=23d93cac-000f-5000-8000-126628f15141"
        },
        "created_at": "2024-04-06T14:30:45.129Z",
        "description": "Заказ №1",
        "metadata": {},
        "recipient": {
            "account_id": Configuration.account_id,
            "gateway_id": "100700"
        },
        "refundable": "false",
        "test": "false"
    }

    payment = Payment.create(payment_data)

    # get confirmation url
    confirmation_url = payment.confirmation.confirmation_url


if __name__ == '__main__':
    app.run(host="0.0.0.0")
