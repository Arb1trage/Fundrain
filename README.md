# Fund-rain
Fund-rain is a simple CLI Web3 wallet funding/distribution tool, targetted towards multiwallet sniper software users and written in Python. It helps snipers to avoid address blacklists, makes dev on-chain analysis more difficult and automates setting up for multiwallet snipe action.

## Features

- Generate multiple, ERC-20 compatible wallets
- Export wallet information to file in sniper-specific format (Coyote, Brownie, PGTS etc.)
- Fund addresses with desired amount of base cryptocurrency from source wallet
- Keep your OPSEC clean when sniping to avoid blacklists and on-chain analysis

## Usage
```sh
cd dillinger
npm i
node app
```

## Installation
Use provided fundrain.exe binary that has built-in dependencies.

OR

Install required packages with
```sh
python3 -m pip install -r requirements.txt
```
then just execute the script with Python.

NOTE: Tool was programmed for Python 3.10, but should work with any Python 3.x version.
