import json
from flask import Flask, jsonify, render_template, request, redirect, url_for, session
from blockchain import Blockchain

app = Flask(__name__)
app.secret_key = 'J72thBOsKO'
blockchain = Blockchain()

users = {
    'admin': 'passwd',
    'JP2': '2137',
    'admin': 'passwd'
}


#login page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        
        # Get the username and password from the login form
        username = request.form.get('username')
        password = request.form.get('password')

        # For simplicity, we'll check for a hardcoded username and password

        if username in users and users[username] == password:
            session['username'] = username         
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
     # Check if the username is stored in the session
    if 'username' in session:
        # Retrieve the username from the session
        username = session['username']
        
        # Render the home page with the username
        return render_template('home.html', username=username)
    else:
        # Redirect to the login page if the username is not found in the session
        return redirect(url_for('login'))

# Mining a new block

@app.route('/mine_block', methods=['GET'])
def mine_block():
	if 'username' in session:
		previous_block = blockchain.print_previous_block()
		previous_proof = previous_block['proof']
		proof = blockchain.proof_of_work(previous_proof)
		previous_hash = blockchain.hash(previous_block)
		block = blockchain.create_block(proof, previous_hash)
                
		response = {'message': 'A block is MINED','index': block['index'],'timestamp': block['timestamp'],'proof': block['proof'],'previous_hash': block['previous_hash']}
		json_data = json.dumps(response)
		return render_template('mine.html', json_data=json_data)
	else:
		return redirect(url_for('login'))
# Display blockchain in json format

@app.route('/get_chain', methods=['GET'])
def display_chain():
    if 'username' in session:
        response = {'chain': blockchain.chain,'length': len(blockchain.chain)}
        json_data = json.dumps(response) 
        return render_template('get_chain.html', json_data=json_data)
    else:
        return redirect(url_for('login'))
          

# Check validity of blockchain


@app.route('/valid', methods=['GET'])
def valid():
	if 'username' in session:
		valid = blockchain.check_chain_validity(blockchain.chain)
		if valid:
			response = {'message': 'The Blockchain is valid.'}
		else:
			response = {'message': 'The Blockchain is not valid.'}
			return jsonify(response), 200
	else:
		return redirect(url_for('login'))
# Run the flask server locally
app.run(host='127.0.0.1', port=5000)


   