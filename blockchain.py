import hashlib
import json
import datetime
from random import randint

class Blockchain:

	def __init__(self):
		self.chain = []
		self.append_block(message='', author='SYSTEM', timestamp=str(datetime.datetime.now()), proof=randint(1,9999999))

	def pow_hash(self,proof1, proof2):
		return hashlib.sha256(str(proof1**2 - proof2**2).encode()).hexdigest()

	def block_hash(self, block):
		encoded_block = json.dumps(block, sort_keys=True).encode()
		return hashlib.sha256(encoded_block).hexdigest()
 
	def append_block(self, message, author, timestamp, proof): #block generation
		if len(self.chain)>0:
			previous_hash = self.block_hash(self.chain[-1])
			previous_proof = self.chain[-1]['proof'] #verifying that block candidate met the requirement
			hash_op = self.pow_hash(proof,previous_proof)
			if hash_op[:5] != '00000':
				return None
		else:
			previous_hash  = '0'

		block = {'index': len(self.chain) + 1,	
				'message': message,
				'author': author, 
				'timestamp': timestamp,
				'proof': proof,
				'previous_hash': previous_hash}
		self.chain.append(block)
		return block

	def proof_of_work(self): #calculating the proof that client can add a block
		previous_proof = self.chain[-1]['proof'] 
		current_proof = 1
		check_proof = False
		while check_proof is False:
			hash_op = self.pow_hash(current_proof,previous_proof) #calculate until first five bytes are 0s
			if hash_op[0:5] == '00000':
				check_proof = True
			else:
				current_proof += 1
		return current_proof

	def check_chain_validity(self): #recalculating of all hashes and proofs
		previous_block = self.chain[0]
		block_index = 1
		while block_index < len(self.chain):
			block = self.chain[block_index]
			if block['previous_hash'] != self.block_hash(previous_block): #checking block integrity
				return False
			previous_proof = previous_block['proof']
			proof = block['proof']
			hash_op = self.pow_hash(proof,previous_proof) #checking if author has actually met the requirements to append a block
			if hash_op[:5] != '00000':
				return False
			previous_block = block
			block_index += 1
		return True

