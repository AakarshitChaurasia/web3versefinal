from django.shortcuts import render
from web3 import Web3

def get_wallet_balance(wallet_address):
    # Connect to Ethereum network using Infura API
    w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/ddbbf46d32a340729806c0de8f417d09'))

    # Convert wallet address to checksum format
    checksum_address = w3.to_checksum_address(wallet_address)

    # Fetch current balance of wallet
    balance_wei = w3.eth.get_balance(checksum_address)

    # Convert balance from wei to ether
    balance_eth = w3.from_wei(balance_wei, 'ether')

    return balance_eth

import requests

def get_recent_transactions(wallet_address):
    # Construct the API endpoint URL
    url = f"https://api.etherscan.io/api?module=account&action=txlist&address={wallet_address}&sort=desc&apikey=K84BK1K78X8I9JQBB4T2VCXYYQQFU5P3MS"

    # Send the HTTP request to the Etherscan API
    response = requests.get(url)

    # Parse the JSON response and extract the transaction data
    tx_list = []
    if response.status_code == 200:
        tx_data = response.json()['result']
        for i in range(min(len(tx_data), 5)):
            tx_dict = {}
            tx_dict['hash'] = tx_data[i]['hash']
            tx_dict['from'] = tx_data[i]['from']
            tx_dict['to'] = tx_data[i]['to']
            tx_dict['value'] = int(tx_data[i]['value']) / pow(10,18)
            tx_list.append(tx_dict)

    return tx_list





def fetch_wallet(request):
    if request.method == 'POST':
        # Get the Ethereum address entered by the user
        wallet_address = request.POST.get('wallet_address')

        # Fetch the current balance of the wallet
        balance = get_wallet_balance(wallet_address)

        # Fetch the five most recent transactions involving this wallet
        transactions = get_recent_transactions(wallet_address)

        # Render the template with the wallet balance, transaction history, and wallet address
        return render(request, 'wallet.html', {'balance': balance, 'transactions': transactions, 'wallet_address': wallet_address})

    # If the request method is not POST, just render the empty form
    return render(request, 'fetch.html')