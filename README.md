[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
# Fundrain
Fundrain is a simple Web3 CLI wallet generation/funding tool, targetted towards multiwallet sniper software users and written in Python.
It helps snipers to avoid address blacklists, makes dev on-chain analysis more difficult and automates setting up for multiwallet snipe action.

## Features

- Generate multiple, ERC-20 compatible wallets
- Export wallet information to file in sniper-specific format (Coyote, Brownie, PGTS etc.)
- Fund addresses with desired amount of base cryptocurrency from source wallet
- Supports most EVM-compatible blockchains 
- Keep your OPSEC clean when sniping to avoid blacklists and on-chain analysis

## Usage
```
usage: fundrain.py [-h] [-V, --version] -w WALLET_QUANT -c {BSC,ETH,CRO,FTM,AVAX,POLY,mADA} [-a AMOUNT] [-m MOTHER_KEY] [-g CUSTOM_GAS] [-y]

options:
  -h, --help            show this help message and exit
  
  -V, --version         show program's version number and exit
  
  -w WALLET_QUANT, --wallets WALLET_QUANT
                        Amount of wallets to generate (Maximum 30).
                        
  -c {BSC,ETH,CRO,FTM,AVAX,POLY,mADA}, --chain {BSC,ETH,CRO,FTM,AVAX,POLY,mADA}
                        Abbreviation of target chain name eg. ETH.
                        
  -a AMOUNT, --amount AMOUNT
                        Optional. If supplied, each generated wallet should receive specified amount of native currency. Required mother wallet
                        balance to perform this action is [ (TX_GAS + AMOUNT) * WALLETS ]. By default, gas price will be based on median value 
                        from recent transactions on chain to ensure safe low price.
                        
  -m MOTHER_KEY, --mother-key MOTHER_KEY
                        Optional. Private key of mother account. If --amount is provided without --mother, will generate one and ask user to 
                        supply it with native chain currency accordingly. In that case, it's included as a sniper when counting --wallets.
                        
  -g CUSTOM_GAS, --gas-price CUSTOM_GAS
                        Optional. If supplied along with --amount, sets gas price (in gwei) to use when distributing funds to wallets. Gas limit 
                        is always set to 21000 and is unchangeable.
                        
  -y                    Optional. Disables prompting for permission on each transaction.
```

## Installation
Install dependencies listed in requirements.txt:
```sh
python3 -m pip install -r requirements.txt
```
then execute like any other .py script:
```sh
chmod +x fundrain.py
./fundrain.py [OPTIONS]
```
NOTE: Tool was programmed to use with Python 3.10, but should work with any Python 3.x version.
