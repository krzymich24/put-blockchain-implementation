import json
from flask import Flask, jsonify, render_template, request, redirect, url_for, session
import datetime
import hashlib
from blockchain import Blockchain

app = Flask(__name__)
app.secret_key = 'J72thBOsKO'
blockchain = Blockchain()

#users list
users = {
    'admin': '0d6be69b264717f2dd33652e212b173104b4a647b7c11ae72e9885f11cd312fb', #passwd
    'Andrzej': '3ec0f5f50dfa5607492c4d1b4f16776f2f9d0c7a787d10a78d187c1172721c91', #andrzej1
    'root': '4813494d137e1631bba301d5acab6e7bb7aa74ce1185d456565ef51d737677b2', #root
}

#login page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get the username and password from the login form
        username = request.form.get('username')
        password = hashlib.sha256(request.form.get('password').encode()).hexdigest()

        if username in users and users[username] == password:
            session['username'] = username         
            # Redirect to the home page if authentication is successful
            return redirect(url_for('home'))
        else:
            # Render the login page with an error message
            error = 'Invalid username or password'
            return render_template('login.html', error=error)
    else:
        return render_template('login.html')

#home page
@app.route('/home')
def home():
     # Check if the username is stored in the session
    if 'username' in session:
        username = session['username']
        return render_template('home.html', username=username)
    else:
        return redirect(url_for('login'))

# Mining a new block
@app.route('/mine_block', methods=['GET', 'POST'])
def mine_block():
    if 'username' in session:
        msg = request.form.get('text_input')   
        author = session['username']
        proof = blockchain.proof_of_work()
        completed_at = str(datetime.datetime.now())
        response = blockchain.append_block(msg, author, completed_at, proof)
        if response is None:
            print('Block discarded.')
                
        json_data = json.dumps(response)
        return render_template('mine.html', json_data=json_data)
    else:
        return redirect(url_for('login'))
        
# Display blockchain in json format
@app.route('/get_chain', methods=['GET'])
def display_chain():
    if 'username' in session:
        return render_template('get_chain.html', chain=blockchain.chain, length=len(blockchain.chain))
    else:
        return redirect(url_for('login'))
          

# Check validity of blockchain
@app.route('/valid', methods=['GET'])
def valid():
    if 'username' in session:
        validity = blockchain.check_chain_validity()

        if validity:
            response = {'message': 'The Blockchain is valid.'}
        else:
            response = {'message': 'The Blockchain is invalid!'}

        json_data = json.dumps(response)
        return render_template('validation.html', json_data=json_data)
    else:
        return redirect(url_for('login'))
    

# Clear the session and redirect to the login page        
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Run the flask server locally
app.run(host='127.0.0.1', port=5000)


   