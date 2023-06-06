import datetime
from blockchain import Blockchain

bc = Blockchain()

#menu
def menu():
    print("")
    print("Blockchain Debugging")
    print("1. Mine a block")
    print("2. Display the chain")
    print("3. Check validity of the chain")
    print("4. Mine a block badly")
    print("5. Exit")
    print("")

#mine a block
def mine_block():
    msg = input("Enter a message: ")
    auth = input("Who wrote this?: ")
    
    proof = bc.proof_of_work()
    completed_at = str(datetime.datetime.now())
    block = bc.append_block(msg, auth, completed_at, proof)
    if block is None:
        print('Block discarded.')
    return block

def mine_block_badly():
    msg = input("Enter a message: ")
    auth = input("Who wrote this?: ")
    
    proof = 00000000 #cheat
    completed_at = str(datetime.datetime.now())
    block = bc.append_block(msg, auth, completed_at, proof)
    if block is None:
        print('Block discarded.')
    return block

#display the chain
def display_chain():
    for block in bc.chain:
        print(block)
    print(f"Length: {len(bc.chain)}")
    return

#check validity of the chain
def validity():
    valid = bc.check_chain_validity()
    if valid:
        print("The Blockchain is valid.")
    else:
        print("The Blockchain is not valid!")
    return

#main
def main():
    while True:
        menu()
        choice = input("Enter your choice: ")
        if choice == "1":
            mine_block()
        elif choice == "2":
            display_chain()
        elif choice == "3":
            validity()
        elif choice == "4":
            mine_block_badly()
        elif choice == "5":
            exit()
        else:
            print("Invalid choice. Try again.")
            continue

if __name__ == "__main__":
    main()