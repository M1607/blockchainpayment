# Client_flask captures and processes the user input through a 
# web form, send the data to the server, and displays a response
# to the user.
#
#
# @author (Maddie Hirschfeld)
# @version (June 6, 2024)

from flask import Flask, render_template, request, jsonify
import socket
import logging
import re
from blockchain.cryptograph import Cryptograph

app = Flask(__name__)
# Secret key that is used for session management
app.secret_key = 'your_secret_key'

# Cryptograph class is initialized with encryption key
# Encryption key used for data encyption
key = 'kTZ_RzqoJrKxHx2qcoQcdU-gKFR5yT2BxKg1Lkunqu4='
cryptograph = Cryptograph(key=key)

# Logging to write to the app.log file
logging.basicConfig(filename='app.log', level=logging.DEBUG)

# Connects to the server to send transaction data and recieve
# a response
def send_transaction_to_server(transaction):
    # Connects to the transaction server
    host = socket.gethostname()
    # Ensure that this port matches the server
    port = 5001
    client_socket = socket.socket()
    client_socket.connect((host, port))
    # Send transaction data to the server
    client_socket.send(transaction.encode())
    data = client_socket.recv(1024).decode()
    client_socket.close()
    return data

# Functions validate user input
# Validates  email address
def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

# Validates state and ensures it is 2 characters
def is_valid_state(state):
    return len(state) == 2 and state.isalpha()

# Validates Zip code ensuring there is 5 numbers
def is_valid_zipcode(zipcode):
    return len(zipcode) == 5 and zipcode.isdigit()

# Validates cc number ensuring that there are 16 numbers
def is_valid_cc_number(cc_number):
    return len(cc_number) == 16 and cc_number.isdigit()

# Validates that the expiration date follows the MM/YY format
def is_valid_expiration(expiration):
    return re.match(r"(0[1-9]|1[0-2])\/([0-9]{2})", expiration)

# Validates the cvv and ensures it is 3 numbers
def is_valid_cvv(cvv):
    return len(cvv) == 3 and cvv.isdigit()

# Renders the HTML form for user input
@app.route('/')
def form():
    return render_template('form.html')

# Handles the form submission by validating input, formatting data,
# sending data to the server, and redirecting to the thank you pag
@app.route('/submit', methods=['POST'])
def submit():
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        street = request.form.get('street')
        street2 = request.form.get('street2')
        city = request.form.get('city')
        state = request.form.get('state')
        zipcode = request.form.get('zipcode')
        cc_number = request.form.get('cc_number')
        expiration = request.form.get('expiration')
        cvv = request.form.get('cvv')
    
        # Ensurse all fields are received before proceeding and submitting form
        if not all([name, email, street, city, state, zipcode, cc_number, expiration, cvv]):
            return "Form data is missing, please fill out all fields.", 400

        # Validates each field
        if not is_valid_email(email):
            raise ValueError("Invalid email address.")

        if not is_valid_state(state):
            raise ValueError("Invalid state.")

        if not is_valid_zipcode(zipcode):
            raise ValueError("Invalid zipcode.")

        if not is_valid_cc_number(cc_number):
            raise ValueError("Invalid credit card number.")

        if not is_valid_expiration(expiration):
            raise ValueError("Invalid expiration date.")

        if not is_valid_cvv(cvv):
            raise ValueError("Invalid CVV.")

        # Encypts sensitive information provided
        encrypted_cc_number = cryptograph.encrypt_data(cc_number)
        encrypted_expiration = cryptograph.encrypt_data(expiration)
        encrypted_cvv = cryptograph.encrypt_data(cvv)

        # Formats the transaction data
        transaction = f"{name}, {email}, {street}, {street2}, {city}, {state}, {zipcode}, {encrypted_cc_number}, {encrypted_expiration}, {encrypted_cvv}"
        # Sends the transaction to the server for a response
        response = send_transaction_to_server(transaction)
    
        # Redirect to the thank you page with the server's response
        return render_template('thankyou.html', message=response)
    except ValueError as ve:
        logging.error(f"Value Error: {ve}")
        return jsonify({"error": "Bad Request", "message": str(ve)}), 400
    except Exception as e:
        logging.error(f"Unexpected Error: {e}")
        return jsonify({"error": "Internal Server Error", "message": "An unexpected error occurred. Please try again later."}), 500

# Error Handler for 400 Bad Request errors
@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Bad Request", "message": str(error)}), 400

# Error Handler for 404 Not Found errors
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not Found", "message": str(error)}), 404

# Error Handler for 500 Internal Server errors
@app.errorhandler(500)
def internal_error(error):
    logging.error(f"Server Error: {error}, Route: {request.url}")
    return jsonify({"error": "Internal Server Error", "message": "An unexpected error occurred. Please try again later."}), 500

# Runs the flask application in debug mode
if __name__ == '__main__':
    app.run(debug=True)