from flask import Flask, redirect
import logging

app = Flask(__name__)


@app.route('/')
def redirect_to_komatbang():
    logging.info('redirecting to komatbang: https://www.instagram.com/komatbang/')
    return redirect('https://www.instagram.com/komatbang/')


@app.route('/health-http')
def health_check_http():
    return 'healthy'


@app.route('/health-https')
def health_check_https():
    return 'healthy'
