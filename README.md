# BCMB - Block Chain Message Board
### An online message broad system based on block chain structure.

<br>

## Introduction
Latest-Version: 2.2

The system stucture of BCMB is a dual system:
1. Web Communication-System
2. Assistant Client-System

Communication Protocol:
* HTTP
* Socket TCP

## Preparation:
Python - 3.0 or above
#### Package Installation:
This external library is available on PyPI, it’s recommended to install it using pip

###### For WS environment:
```
pip install ecdsa
```
```
pip install flask
```
```
pip install pycryptodome
```
```
pip install pandas
```
###### For AS environment:
```
pip install ecdsa
```
```
pip install requests
```

Reference Doc: [Python ecdsa](https://github.com/warner/python-ecdsa)

<br>

## How to use
cd to Puff folder and execute `python puff.py`

cd to Sherry folder and execute `python sherry.py`

and you can lauch BCMB on your inner Network

<br>

## Puff - Web Communication System
Puff is the system name of BCMB - WS
Version: 2.2
#### Main Function
* `web_server` - open Flask web server
* `serve` - open Socket server
* `usher` - collect socket client into queue
* `security_check` - keep checking whether if the chain had been modified illegally
* `dashboard` - open the Command Dashboard

<br>

## Sherry - Assistant Client System
Sherry is the system name of BCMB - AS
Version: 1.2
#### Main Function
* `use_service` - dealing the requests typed from clients
* call worker function to acquire certain service

<br>

## Service on BCMB
1. Sign up
2. Sign in
3. Set key
4. Push comment
5. Get my comment
6. Get the rank
7. Get chain JSON
8. Chat with Sherry

<br>

## Key
Clients need keys to use the service on BCMB
* Public Key
* Private Key
* User Key

<br>

## Rules of BCMB
#### Difficulty: 5
#### Hash Type: sha256
#### X Hash - valid block hash of BCMB
#### BMC - Block Mining Certification
#### PAC - Push-comment Authorization Code
#### License
#### BCA - Block Created Application
#### Signature - the verified method base on ecdsa
#### PSV - Person Verification
#### Proof Verification
