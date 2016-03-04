# 英语词典

There is a live demo. http://ladrift.cn:90

## Prerequisite

- Python >= 3.4
- aiohttp >=  0.19.0

## Run on local

Recommend using virtual environment with pyvenv

``` bash
python3 -m venv VENV
source VENV/bin/activate
```

Install the requirements

``` bash
pip install aiohttp
```

And then, run the server

``` bash
python server.py
```

You can go to http://localhost:8000 to see the local running web app.

## Deploy

Follow the guide on aiohttp document [Deployment using Gunicorn](http://aiohttp.readthedocs.org/en/stable/gunicorn.html) and the gunicorn document [Deploying Gunicorn](http://docs.gunicorn.org/en/latest/deploy.html).

