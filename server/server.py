#!/usr/bin/env python3.6
# -*- coding: utf-8 -*- 
"""
server.py
Python 3.6 or newer required.
"""

import stripe
import json
import os
import uuid

import sqlite3
from flask import Flask, render_template, jsonify, request, send_from_directory
from dotenv import load_dotenv, find_dotenv

import nltk
from nltk.tokenize import sent_tokenize
from nltk import pos_tag, word_tokenize
import spacy

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# Setup Stripe python client library
load_dotenv(find_dotenv())
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
stripe.api_version = os.getenv('STRIPE_API_VERSION')

static_dir = str(os.path.abspath(os.path.join(__file__ , "..", os.getenv("STATIC_DIR"))))
print(static_dir)
app = Flask(__name__, static_folder=static_dir,
            static_url_path="", template_folder=static_dir)

@app.route("/", methods=['GET'])
@app.route("/home", methods=['GET'])
@app.route("/index", methods=['GET'])
def home():
    # Display checkout page
    return render_template('index.html')

@app.route('/checkout', methods=['GET'])
def get_checkout_page():
    # Display checkout page
    return render_template('checkout.html')


def calculate_order_amount(items):
    # Replace this constant with a calculation of the order's amount
    # Calculate the order total on the server to prevent
    # people from directly manipulating the amount on the client
    return 100

@app.route('/create-payment-intent', methods=['POST'])
def create_payment():
    customer_id = uuid.uuid1()
    data = json.loads(request.data)
    # Create a PaymentIntent with the order amount and currency
    intent = stripe.PaymentIntent.create(
        amount=calculate_order_amount(data['items']),
        currency=data['currency']
    )
    db = sqlite3.connect('api.db')
    cursor = db.cursor()
    cursor.execute('''INSERT INTO tok(pi, tok)
                   VALUES(?,?)''', (str(intent.id), str(customer_id)))
    db.commit()
    try:
        # Send publishable key and PaymentIntent details to client
        return jsonify({'publishableKey': os.getenv('STRIPE_PUBLISHABLE_KEY'), 'clientSecret': intent.client_secret, 'customer_id': customer_id})
    except Exception as e:
        return jsonify(error=str(e)), 403


@app.route('/webhook', methods=['POST'])
def webhook_received():
    # You can use webhooks to receive information about asynchronous payment events.
    # For more about our webhook events check out https://stripe.com/docs/webhooks.
    webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET')
    request_data = json.loads(request.data)

    if webhook_secret:
        # Retrieve the event by verifying the signature using the raw body and secret if webhook signing is configured.
        signature = request.headers.get('stripe-signature')
        try:
            event = stripe.Webhook.construct_event(
                payload=request.data, sig_header=signature, secret=webhook_secret)
            data = event['data']
        except Exception as e:
            return e
        # Get the type of webhook event sent - used to check the status of PaymentIntents.
        event_type = event['type']
    else:
        data = request_data['data']
        event_type = request_data['type']
    data_object = data['object']

    if event_type == 'payment_intent.succeeded':
        print('💰 Payment received!')
        db = sqlite3.connect('api.db')
        cursor = db.cursor()
        cursor.execute('''UPDATE tok SET stats = ? WHERE pi = ? ''',
                       ('succeeded', data_object['id']))
        db.commit()
        # Fulfill any orders, e-mail receipts, etc
        # To cancel the payment you will need to issue a Refund (https://stripe.com/docs/api/refunds)
    elif event_type == 'payment_intent.payment_failed':
        print('❌ Payment failed.')
        db = sqlite3.connect('api.db')
        cursor = db.cursor()
        cursor.execute('''UPDATE tok SET stats = ? WHERE pi = ? ''',
                       ('failed', data_object['id']))
        db.commit()
    return jsonify({'status': 'success'})


def tok_validate(tok):
    db = sqlite3.connect('api.db')
    cursor = db.cursor()
    cursor.execute("select stats from tok where tok='{}'".format(str(tok)))
    results = cursor.fetchall()
    status = results[0][0]
    return status

@app.route('/1pound-nlp/api/v1.0/tokenize', methods=['POST'])
def tokenize():
    if not request.json or not 'text' in request.json or not request.headers.get('api_tok'):
        return jsonify('Invalid Payload'), 400
    tok=request.headers.get('api_tok')
    status=tok_validate(tok)
    if status == 'succeeded' :
        txt = request.json['text']
        result=sent_tokenize(txt)
        return jsonify({'result': result}), 200
    else:
        return jsonify('Invalid API Token'), 403

@app.route('/1pound-nlp/api/v1.0/tag', methods=['POST'])
def tag():
    if not request.json or not 'text' in request.json or not request.headers.get('api_tok'):
        return jsonify('Invalid Payload'), 400
    tok=request.headers.get('api_tok')
    status=tok_validate(tok)
    if status == 'succeeded' :
        txt = request.json['text']
        result= pos_tag(word_tokenize(txt))
        return jsonify({'result': result}), 200
    else:
        return jsonify('Invalid API Token'), 403

@app.route('/1pound-nlp/api/v1.0/ent', methods=['POST'])
def ent():
    if not request.json or not 'text' in request.json or not request.headers.get('api_tok'):
        return jsonify('Invalid Payload'), 400
    tok=request.headers.get('api_tok')
    status=tok_validate(tok)
    if status == 'succeeded' :
        nlp = spacy.load("en_core_web_sm")
        txt = request.json['text']
        doc = nlp(txt)
        result = []
        for entity in doc.ents:
            result.append([entity.text, entity.label_])
        return jsonify({'result': result}), 200
    else:
        return jsonify('Invalid API Token'), 403

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

