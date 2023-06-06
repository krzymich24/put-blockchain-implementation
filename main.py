import datetime
import hashlib
import json
from flask import Flask, jsonify, render_template, request, redirect, url_for
from blockchain import Blockchain

app = Flask(__name__)
blockchain = Blockchain()

#login page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get the username and password from the login form
        username = request.form['username']
        password = request.form['password']

        # Perform your authentication logic here
        # For simplicity, we'll check for a hardcoded username and password
        if (username == 'admin' and password == 'passwd')or(username == 'JP2' and password == '2137'):
            # Redirect to the home page if authentication is successful
            return redirect(url_for('home'))
        else:
            # Render the login page with an error message
            error = 'Invalid username or password'
            return render_template('login.html', error=error)
    else:
        # Render the login page
        return render_template('login.html')

#home page
@app.route('/home')
def home():
    # Render the home page
    return render_template('home.html')

# Mining a new block

@app.route('/mine_block', methods=['GET'])
def mine_block():
	previous_block = blockchain.print_previous_block()
	previous_proof = previous_block['proof']
	proof = blockchain.proof_of_work(previous_proof)
	previous_hash = blockchain.hash(previous_block)
	block = blockchain.create_block(proof, previous_hash)

	response = {'message': 'A block is MINED',
				'index': block['index'],
				'timestamp': block['timestamp'],
				'proof': block['proof'],
				'previous_hash': block['previous_hash']}

	json_data = json.dumps(response) 

	return render_template('mine.html', json_data=json_data)

# Display blockchain in json format

@app.route('/get_chain', methods=['GET'])
def display_chain():
    
	response = {'chain': blockchain.chain,
				'length': len(blockchain.chain)}

	json_data = json.dumps(response) 
	print(json_data)
	return render_template('get_chain.html', json_data=json_data)

# Check validity of blockchain


@app.route('/valid', methods=['GET'])
def valid():
	valid = blockchain.chain_valid(blockchain.chain)

	if valid:
		response = {'message': 'The Blockchain is valid.'}
	else:
		response = {'message': 'The Blockchain is not valid.'}
	return jsonify(response), 200


# Run the flask server locally
app.run(host='127.0.0.1', port=5000)


   