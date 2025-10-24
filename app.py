from datetime import datetime, timedelta
from flask import Flask, jsonify, render_template, request, send_file
from repository.database import db
from models.payment import Payment
from utils.payments.pix import Pix

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'SECRET_KEY_WEBSOCKET' 

db.init_app(app)


@app.route("/payments/pix", methods=["POST"])
def create_payment_pix():

    data = request.get_json() 

    # validations
    if 'value' not in data:
        return jsonify({"message": "Invalid value"}), 400
    
    expiration_date = datetime.now() + timedelta(minutes=30)

    new_payment = Payment(value= data['value'], expiration_date= expiration_date) #type: ignore

    pix_obj = Pix()
    data_payment_pix = pix_obj.create_payment()
    new_payment.bank_payment_id = data_payment_pix['bank_payment_id']
    new_payment.qr_code = data_payment_pix['qr_code_path']

    db.session.add(new_payment)
    db.session.commit()

    return jsonify({"message": "The payment has benn created!",
                    "payment": new_payment.to_dict()})


@app.route("/payments/confirmation", methods=["POST"])
def pix_confirmation():
    return jsonify({"message": "The payment has benn confirmed!"})

@app.route('/payments/pix/<int:payment_id>', methods=["GET"])
def payment_pix_page(payment_id):
    return render_template('payment.html')

@app.route("/payments/pix/qr_code/<file_name>", methods=['GET'])
def payments_pix_qrcode(file_name):
    return send_file(f"static/img/{file_name}.png", mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True)
