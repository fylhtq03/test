from flask import Flask, render_template, request
from yookassa import Configuration, Payment
import requests

podpislon_api_key = 'your_api_key'
Configuration.account_id = 'shop_id'
Configuration.secret_key = 'secret_key'
Configuration.timeout = 60

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
    Payment_create()
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

def Payment_create():
    # Создание объекта Payment
    payment = Payment.create({
        "amount": {
            "value": "10.00",
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "http://127.0.0.1:5000"
        },
        "description": "Оплата услуги"
    })

    # Получение ссылки на оплату
    payment_url = payment.confirmation.confirmation_url
    print(payment_url)


if __name__ == '__main__':
    app.run(host="0.0.0.0")