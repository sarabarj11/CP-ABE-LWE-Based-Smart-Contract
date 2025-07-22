import flask
from flask import Flask, json, request, jsonify, render_template, url_for, redirect
import numpy as np
from random import randint
from numpy.random import normal
import math
from math import log
import sympy
from sympy import *
import json
import requests
from jinja2 import Environment, FileSystemLoader
import sys
import json_tricks as json 
import urllib.request
import urllib.parse
import os
from json_tricks import load

from flask_restful import Api, Resource
from web3 import Web3

# Initialize Flask app
app = Flask(__name__)

#app.config['JSONIFY_TIMEOUT'] = 3600

# Configure Ethereum provider (Ganache)
ganache_url = 'http://localhost:7545'  # Update with your Ganache node URL
w3 = Web3(Web3.HTTPProvider('http://localhost:7545', request_kwargs={'timeout': 3600}))

print(w3.is_connected())

# Contract ABI and address
contract_address = "0xd385d6b0e0D7D96eB4a36e540c3946808691315d"  # Update with your contract address
contract_abi = None  # Initialize the ABI variable
# Load the ABI (Application Binary Interface) of the smart contract
with open('../build/contracts/QuantumSecureAccessControl.json') as f:
    info_json = json.load(f)
contract_abi = info_json['abi']

# Create a contract instance
contract = w3.eth.contract(address=contract_address, abi=contract_abi)





# Increase the timeout (default is 300 seconds)
#app.config['SERVER_NAME'] = 'localhost:5000'  # Modify to match your server address
#app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000  # Optional: Caching duration
#app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # Optional: Session timeout


app = Flask(__name__,  template_folder='templates')
#api =   Api(app)


def text_to_bit_matrix(text):
    # Initialize an empty matrix
    matrix = []

    # Iterate through each character in the text
    for char in text:
        # Convert the character to its binary representation (8 bits)
        binary_representation = format(ord(char), '08b')

        # Append each bit as a separate element in the row
        matrix.append([int(bit) for bit in binary_representation])

    return matrix

def bit_matrix_to_text(bit_matrix):
    text = ""
    for row in bit_matrix:
        
        # Convert the binary row into an integer
        char_code = int(''.join(map(str, row)),2)
        
        # Convert the integer to a character and append it to the text
        text += chr(char_code)
    return text




@app.route('/', methods=['GET'])
def home():    
    return render_template('index2.html')
    
@app.route('/api/pvkeysgen/', methods=['GET','POST'])
def PvKeysGen() :
    if request.method == 'POST': 
        try: 
            m = int(request.form['m'])
            general_policy = request.files['general_policy']
            service = request.form['service']
            file_data= general_policy.read()
            data = json.loads(file_data, conv_str_byte=True)
            if service in list(data.keys()): 
                results1 = {'service':service}
                policy = data[service]
                attributes_policy = policy.split(' and ')
                for attribute in attributes_policy:
                    q = sympy.randprime(m**2,2*(m**2))
                    n = round(1.1*m*math.log(q))
                    S = np.random.randint(q, size=(n, 1)) 
                    pvkey_attribute = S.tolist(),q,m
                    results1[attribute] = pvkey_attribute
                return json.dumps(results1)
        except:  
            return jsonify("You can't get a private key")
    elif request.method == 'GET':
        return render_template('genpvkey.html')
        
@app.route('/api/pubkeysgen/', methods=['GET','POST'])
def PubKeysGen() :
    if request.method == 'POST': 
        try: 
            pvkey1 = request.files['file']
            file_data= pvkey1.read()
            data = json.loads(file_data, conv_str_byte=True)
            service = data['service']
            results1 = {'service':service}
            for attribute in list(data.keys()):
                if attribute not in {"None", None, 'None'}:
                    if attribute != 'service':
                        pvkey_attribute = data[attribute]
                        m = int(pvkey_attribute[2])
                        alpha = 1 / (math.sqrt(m) * math.log(m)**2)
                        q = int(pvkey_attribute[1])
                        n = round(1.1*m*math.log(q))
                        S = np.matrix(pvkey_attribute[0])
                        A = np.random.randint(q, size=(m, n)) 
                        E1 = np.around([[int(np.random.normal(0,alpha / math.sqrt(2 * math.pi))) for i in range(1)] for j in range(m) ])
                        P1 = np.mod(np.matmul(A,S) + E1, q)
                        pubkey_attribute = A.tolist(),q,P1.tolist()
                        results1[attribute] = pubkey_attribute
            return json.dumps(results1)    
        except: 
            return jsonify("You can't get a public key")  
    elif request.method == 'GET':
        return render_template('genpubkey.html')

@app.route('/api/encrypt/', methods=['GET','POST'])
def Encrypt():  
    if request.method == 'POST':        
        try:
            json_file = request.files['pubkey']
            user_attributes = request.files['Attributes']
            user_policy = request.files['user_policy']
            service = request.form['service']
            file_data = json_file.read()    
            data = json.loads(file_data, conv_str_byte=True)
            file_data2 = user_attributes.read()    
            data2 = json.loads(file_data2, conv_str_byte=True)
            file_data3 = user_policy.read()    
            data3 = json.loads(file_data3, conv_str_byte=True)
            if service in list(data3.keys()):
                attributes_policy = data3[service].split(' and ')
                results2 = {}
                for attribute in attributes_policy:
                    if attribute not in {'service', 'None', None, "None"}:        
                        pubkey_attribute = data[attribute]
                        A = np.matrix(pubkey_attribute[0])
                        P1 = np.matrix(pubkey_attribute[2])
                        attribute1 = text_to_bit_matrix(data2[attribute])               
                        q = np.matrix(pubkey_attribute[1])
                        n = A.shape[0]
                        m = A.shape[1] 
                        a = np.random.randint(2,size=(n,1))
                        u = np.matmul(np.transpose(A), a)
                        c1 = np.matmul(np.transpose(P1), a) 
                        i = len(attribute1)
                        c = c1[0][0]
                        delta = np.ones((i,8))
                        for i1 in range(i):
                            for j1 in range(8):
                                delta[i1][j1] = np.mod((np.around(q * attribute1[i1][j1] / 2) + c), q)
                        delta= delta.astype(int).tolist()
                        u = u.tolist()
                        Cipher= [delta,u]
                        results2[attribute] = Cipher
                return json.dumps(results2)
        except:   
            return jsonify("You can't perform encryption")
    elif request.method == 'GET':
        return render_template('results2.html')
        

#The decryption function
@app.route('/api/decrypt/', methods=['GET','POST'])
def Decrypt():
    if request.method == 'POST':
        try:
            json_file = request.files['file']
            json_file1 = request.files['file1']
            file_data = json_file.read()
            file_data3= json_file1.read()
            data = json.loads(file_data, conv_str_byte=True)
            data3= json.loads(file_data3, conv_str_byte=True)  
            result = {}
            for attribute in list(data3.keys()):
                if attribute not in {'service', 'None', None}:  
                    pvkey_attribute = data[attribute]
                    S = np.matrix(pvkey_attribute[0])
                    C = np.matrix(data3[attribute][0])
                    u = np.matrix(data3[attribute][1])
                    q = pvkey_attribute[1]
                    i = C.shape[0]
                    j = C.shape[1]
                    T = np.array(np.matmul(np.transpose(S), u))
                    a = np.ones((i,j))
                    b = np.ones((i,j))
                    for i1 in range(i):
                        for j1 in range(j):
                            a[i1][j1] = np.mod((int(np.array(C)[i1][j1]) - int(T[0][0])),q)        
                            b[i1][j1] = np.mod(np.around(2*a[i1][j1]/q),q)  
                    plaintext = bit_matrix_to_text(b.astype(int))
                    result[attribute] = plaintext    
            return json.dumps(result)
        except:
            return jsonify("Unauthorized Access")
    elif request.method == 'GET':
        return render_template('results3.html')




@app.route('/grant_access', methods=['GET','POST'])
def grant_access():
    if request.method == 'POST':
        private_key = request.form['private_key'] 
        service = request.form['service']
        user_attributes = request.files['Attributes']
        user_policy = request.files['user_policy']
        json_file = request.files['pubkey']
        user_address = w3.eth.account.from_key(private_key).address
        encrypted_attributes = f"{Encrypt()}"
        # Grant access
        access = contract.functions.grantAccess(user_address, service, encrypted_attributes).transact({'from': user_address})
        
        # Wait for the transaction to be mined
        w3.eth.wait_for_transaction_receipt(access)
        # Retrieve the return value by calling the contract's view function
        ciphertext = contract.functions.hasAccess(user_address, service).call({'from': user_address})
        return f"{ciphertext}"  
    elif request.method == 'GET':
        return render_template('grant_access.html')
        
@app.route('/revoke_access', methods=['GET','POST'])
def revoke_access():
    if request.method == 'POST':
        private_key = request.form['private_key']
        service = request.form['service']
        user_address = w3.eth.account.from_key(private_key).address
        # Revoke access by sending the user address and service to the contract
        tx_hash = contract.functions.revokeAccess(user_address, service).transact({'from': user_address})
        # Wait for the transaction to be mined
        w3.eth.wait_for_transaction_receipt(tx_hash)
        return jsonify({"message": "Acces revokked successfully"}), 201
    elif request.method == 'GET':
        return render_template('revoke_access.html')
     
@app.route('/check_access', methods=['GET','POST'])
def check_access():
    if request.method == 'POST':
        user_address = request.form['user_address']
        service = request.form['service']
        json_file = request.files['file']
        file_data = json_file.read()
        file_data3 = f"{contract.functions.hasAccess(user_address, service).call()}"
        data = json.loads(file_data, conv_str_byte=True)
        try: 
            data3= json.loads(file_data3, conv_str_byte=True)  
            result = {}
            for attribute in list(data3.keys()):
                if attribute not in {'service', 'None', None}:  
                    pvkey_attribute = data[attribute]
                    S = np.matrix(pvkey_attribute[0])
                    C = np.matrix(data3[attribute][0])
                    u = np.matrix(data3[attribute][1])
                    q = pvkey_attribute[1]
                    i = C.shape[0]
                    j = C.shape[1]
                    T = np.array(np.matmul(np.transpose(S), u))
                    a = np.ones((i,j))
                    b = np.ones((i,j))
                    for i1 in range(i):
                        for j1 in range(j):
                            a[i1][j1] = np.mod((int(np.array(C)[i1][j1]) - int(T[0][0])),q)        
                            b[i1][j1] = np.mod(np.around(2*a[i1][j1]/q),q)  
                    
                    plaintext = bit_matrix_to_text(b.astype(int))
                    result[attribute] = plaintext    
            return jsonify(result)
        except:
            return jsonify("Unauthorized Access")
    elif request.method == 'GET':
        return render_template('check_access.html')

@app.route('/generate_user', methods=['POST','GET'])
def generate_user():
    if request.method == 'POST':
        private_key = request.form['user_address']
        user_policy = request.files['user_policy']
        encryptedAttributes = request.files['Attributes']
        service = request.form['service']
        json_file = request.files['pubkey']
        user_address = w3.eth.account.from_key(private_key).address
        # Check if user is already registered
        file_data1= encryptedAttributes.read()
        file_data2= user_policy.read()
        encrypted_attributes = f"{Encrypt()}"          
        
        tx_hash = contract.functions.setUserAttributes(user_address, str(policy), str(service), str(encryptedAttributes1)).transact({'from': user_address})
        # Wait for the transaction to be mined
        w3.eth.wait_for_transaction_receipt(tx_hash)
        return jsonify({"message": "User registered successfully"}), 201
    elif request.method == 'GET':
        return render_template('genuser.html')


if __name__ == '__main__':
     #app.run(debug=True, threaded=True, port=5000, host='localhost', use_reloader=False, **{'threaded': True})
     app.run(debug = True)
