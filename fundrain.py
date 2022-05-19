import time
import binascii 
import argparse
import click
from sys import exit
from pathlib import Path
from web3 import Web3


NETWORKS = {
    'BSC': {'rpc': 'https://bsc-dataseed.binance.org/', 'chain_id': 56, 'explorer': 'https://bscscan.com/tx/', 'ticker': 'BNB'},
    'ETH': {'rpc': 'https://mainnet.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161', 'chain_id': 1, 'explorer': 'https://etherscan.io/tx/', 'ticker': 'ETH'},  
    'CRO': {'rpc': 'https://evm-cronos.crypto.org/', 'chain_id': 25, 'explorer': 'https://cronoscan.com/tx/', 'ticker': 'CRO'},
    'FTM': {'rpc': 'https://rpc.fantom.network', 'chain_id': 250, 'explorer': 'https://cronoscan.com/tx/', 'ticker': 'FTM'},
    'AVAX': {'rpc': 'https://api.avax.network/ext/bc/C/rpc', 'chain_id': 43114, 'explorer': 'https://snowtrace.io/tx/', 'ticker': 'AVAX'},
    'POLY': {'rpc': 'https://polygon-rpc.com', 'chain_id': 137, 'explorer': 'https://polygonscan.com/tx/', 'ticker': 'MATIC'},
    'mADA': {'rpc': 'https://rpc-mainnet-cardano-evm.c1.milkomeda.com/', 'chain_id': 2001, 'explorer': 'https://explorer-mainnet-cardano-evm.c1.milkomeda.com/tx/', 'ticker': 'mADA'}
}

# TESTNETS
# NETWORKS = {
#     'BSC': {'rpc': 'https://data-seed-prebsc-1-s1.binance.org:8545', 'chain_id': 97, 'explorer': 'https://testnet.bscscan.com/tx/', 'ticker': 'BNB'},
#     'ETH': {'rpc': 'https://ropsten.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161', 'chain_id': 3, 'explorer': 'https://ropsten.etherscan.io/tx/', 'ticker': 'ETH'},  
#     'CRO': {'rpc': 'https://cronos-testnet-3.crypto.org:8545/', 'chain_id': 338, 'explorer': 'https://cronos.org/explorer/testnet3/tx/', 'ticker': 'CRO'},
#     'FTM': {'rpc': 'https://rpc.testnet.fantom.network', 'chain_id': 4002, 'explorer': 'https://testnet.ftmscan.com/tx/', 'ticker': 'FTM'},
#     'AVAX': {'rpc': 'https://api.avax-test.network/ext/bc/C/rpc', 'chain_id': 43113, 'explorer': 'https://testnet.snowtrace.io/tx/', 'ticker': 'AVAX'},
#     'POLY': {'rpc': 'https://matic-mumbai.chainstacklabs.com', 'chain_id': 80001, 'explorer': 'https://mumbai.polygonscan.com/tx/', 'ticker': 'MATIC'},          
#     'mADA': {'rpc': 'https://rpc-devnet-cardano-evm.c1.milkomeda.com/', 'chain_id': 200101, 'explorer': 'https://explorer-devnet-cardano-evm.c1.milkomeda.com/tx/', 'ticker': 'mADA'}   
# }



def validate_privkey(priv_key: str):
    try:
        wallet = Web3(None).eth.account.from_key(priv_key)
        return (wallet._private_key).hex()
    except (binascii.Error, ValueError):
        print("Error: Invalid private key or it's format")
        exit()


def validate_float(user_input: str):
    try:
        amount = round(float(user_input), 3)
        if amount > 0:
            return amount
        else:
            return ValueError
    except (TypeError, ValueError):
        print("Error: Amount and/or gas price must be positive numbers.")
        exit()


def validate_wallet_quant(user_input: str):
    try:
        wallet_quantity = int(user_input)
        if wallet_quantity in range(1,31):
            return wallet_quantity
        else:
            raise ValueError
    except (TypeError, ValueError):
        print("Error: Wrong number of wallets.")
        exit()


def validate_chain(user_input: str):
    try:
        if user_input in NETWORKS.keys():
            return user_input
        else:
            raise ValueError
    except (TypeError, ValueError):
        print("Error: Chain not supported.")
        exit()
        
        
def check_arg_combinations(amount: float|None, custom_gas: float|None, mother_key: str|None):
    try:
        if (amount is None) \
            and ((custom_gas is not None) or (mother_key is not None)):
            raise ValueError
    except ValueError:
        print("Error: Used --mother or --gas-price without specifying --amount.")
        exit()
        


def generate_wallets(quantity: int):
    try:
        wallets = [W3.eth.account.create() for i in range(quantity)]
        return wallets
    except Exception as e:
        print(f"Error while generating wallets: {repr(e)}")
        exit()


def export_wallets(wallets: list, chain:str):
    try:
        Path("wallets").mkdir(parents=True, exist_ok=True)
        with open(f"wallets/wallets_{chain}_{time.strftime('%y%m%d-%H%M%S')}.txt", 'w') as file:
            file.write(f"{chain}:\n")
            for idx, wallet in enumerate(wallets):
                priv_key = (wallet._private_key).hex()[2:]
                pub_addr = (wallet._address)
                file.write(f"{priv_key} {chain}_{idx} {pub_addr}\n")
        print(f"\nWallets successfully exported to file: {file.name}\n")
        Path()
    except Exception as e:
        print(f"Error while exporting wallets: {repr(e)}")
        exit()


def print_wallets(wallets: list, chain: str):
    print("Wallets and current balance:")
    for idx, wallet in enumerate(wallets):
        balance_in_eth = W3.fromWei(W3.eth.get_balance(wallet._address),'ether')
        if idx == 0:
            print(f"{chain}_{idx} {wallet._address} ({balance_in_eth} {NETWORKS[args.chain]['ticker']}) (Mother)")
        else:
            print(f"{chain}_{idx} {wallet._address} ({balance_in_eth} {NETWORKS[args.chain]['ticker']})")
    print()
             
             
def calc_needed_funds(wallet_quantity: int, amount: float, custom_gas=None):
    needed_funds = (calc_tx_gas_in_eth(custom_gas) + amount) * wallet_quantity
    return needed_funds


def calc_tx_gas_in_eth(custom_gas=None):
    if custom_gas is None:
        tx_gas_in_eth = float(W3.fromWei(W3.eth.gasPrice * 21000, 'ether'))*1.05
    else:
        tx_gas_in_eth = float(W3.fromWei(W3.toWei(custom_gas, 'gwei') * 21000, 'ether'))*1.05
    return tx_gas_in_eth


def transfer(chain, wallet_from, wallet_to, amount, custom_gas=None):
    """Transfers specified amount of base currency from one wallet to another.

    Args:
        chain (string): _description_
        wallet_from (Web3.eth.account): _description_
        wallet_to (Web3.eth.account): _description_
        amount (float): Amount of base currency to transfer.
        custom_gas (float, optional): Custom gas price (gwei) used for transaction. Defaults to None.

    Returns:
        (string, HexBytes): A tuple containing, respectively, a string (transaction URL) and HexBytes (transaction hash).
    """

    tx = {
        'chainId': NETWORKS[chain]['chain_id'],
        'nonce': W3.eth.get_transaction_count(wallet_from._address),
        'to': wallet_to._address,
        'value': W3.toWei(amount, 'ether'),
        'gas': 21000,
        'gasPrice': W3.eth.gasPrice
    }
    if custom_gas is not None:
        tx['gasPrice'] = W3.toWei(custom_gas, 'gwei')
    signed_tx = wallet_from.sign_transaction(tx)
    tx_hash = W3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_link = f"{NETWORKS[chain]['explorer']}{W3.toHex(tx_hash)}"
    return (tx_link, tx_hash)


def main(args):
    global W3
    W3 = Web3(Web3.HTTPProvider(NETWORKS[args.chain]['rpc']))
    print('Fundrain by Arb1trage - Version 1.0')
    
    wallets = generate_wallets(args.wallet_quant)
    ticker = NETWORKS[args.chain]['ticker']
    if args.mother_key is not None:
        wallets[0] = W3.eth.account.from_key(args.mother_key)
    export_wallets(wallets, args.chain)
    print_wallets(wallets, args.chain)
    
    if args.amount is None:
        exit()
    else:
        mother_wallet = wallets[0]
        while True:
            required_balance = calc_needed_funds(args.wallet_quant, args.amount, args.custom_gas)
            mother_balance = W3.fromWei(W3.eth.get_balance(mother_wallet._address), 'ether')
            if mother_balance >= required_balance:
                for wallet in wallets[1:]:
                    gas_in_ether = round(calc_tx_gas_in_eth(args.custom_gas), 5)
                    prompt = f"Sending {args.amount} {ticker} to {wallet._address}. Estimated gas: {gas_in_ether} {ticker}. Confirm?"
                    try:
                        if args.skip_prompts is True:
                            print(prompt[:-10])
                            tx_link, tx_hash = transfer(args.chain, mother_wallet, wallet, args.amount, args.custom_gas)
                            print(f"Transaction sent: {tx_link}")
                            print("Processing...", end='', flush=True)
                            if(W3.eth.wait_for_transaction_receipt(tx_hash)):
                                print(" Confirmed!\n")
                                pass
                        else:
                            if click.confirm(prompt, default=True):
                                tx_link, tx_hash = transfer(args.chain, mother_wallet, wallet, args.amount, args.custom_gas)
                                print(f"Transaction sent: {tx_link}")
                                print("Processing...", end='', flush=True)
                                if(W3.eth.wait_for_transaction_receipt(tx_hash)):
                                    print(" Confirmed!\n")
                                    pass
                            else: 
                                raise click.exceptions.Abort
                    except click.exceptions.Abort:
                        print(f"\n\nUser exit: ABORTED")
                        exit()                        
                    except KeyboardInterrupt:
                        print(f"\nUser exit: Be sure to check if transaction was sent")
                        exit()
                    except Exception as e:
                        print(f"\nError response while sending transaction: {repr(e)}")
                        exit()
                print_wallets(wallets, args.chain)
                print("Distribution successful. Check output file for exported keys.")
                exit()
            else:
                try:
                    prompt = f"Required mother wallet balance: {round(required_balance*1.001, 5)} {ticker} (Current balance: {mother_balance} {ticker})"+\
                        "\nAdd funds to wallet and confirm to proceed:"
                    if click.confirm(prompt, default=True):
                        print()
                        pass
                    else:
                        print(f"\nUser exit: ABORTED")
                        exit()
                except (KeyboardInterrupt, click.exceptions.Abort):
                    print(f"\n\nUser exit: ABORTED")
                    exit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Sniper one-time wallets generator. Generates specified '
        'number of private key / address (EIP55) pairs and saves them in a file. '
        'Depending on user choice, can also distribute native chain currency from \"mother\" wallet to '
        'newly generated sniper addresses.')
    parser.add_argument('-V, --version',
                        action='version',
                        version='SniperGenerator by Arb1trage - Version 1.0')
    parser.add_argument('-w', '--wallets',
                        dest='wallet_quant',
                        type=validate_wallet_quant,
                        required=True,
                        help='Amount of wallets to generate (Maximum 30).')
    parser.add_argument('-c', '--chain',
                        dest='chain',
                        type=validate_chain,
                        choices=NETWORKS.keys(),
                        required=True,
                        help='Abbreviation of target chain name eg. ETH.')
    parser.add_argument('-a', '--amount',
                        dest='amount',
                        type=validate_float,
                        required=False,
                        help='Optional. If supplied, each generated wallet should receive specified amount of native '
        'currency. Required mother wallet balance to perform this action is [ (TX_GAS + AMOUNT) * WALLETS ]. By default, '
        'gas price will be based on median value from recent transactions on chain to ensure safe low price.')
    parser.add_argument('-m', '--mother-key',
                        dest='mother_key',
                        type=validate_privkey,
                        required=False,
                        help='Optional. Private key of mother account. If --amount is provided without --mother, '
        'will generate one and ask user to supply it with native chain currency accordingly. '
        'In that case, it\'s included as a sniper when counting --wallets.')
    parser.add_argument('-g', '--gas-price',
                        dest='custom_gas',
                        type=validate_float,
                        required=False,
                        help='Optional. If supplied along with --amount, sets gas price (in gwei) to use when '
        'distributing funds to wallets. Gas limit is always set to 21000 and is unchangeable.')
    parser.add_argument('-y',
                        dest='skip_prompts',
                        action='store_true',
                        help='Optional. Disables prompting for permission on each transaction.')
    # parser.add_argument('-l', '--gas-limit',
    #                     dest='user_limit',
    #                     type=validate_limit,
    #                     required=False,
    #                     help='Optional. Allows to set gas limit for transactions funding sniper wallets. '
    #   'Gas limit is set to 21000 by default.)
    args = parser.parse_args()
    check_arg_combinations(args.amount, args.custom_gas, args.mother_key)
    main(args)
