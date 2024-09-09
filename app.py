from flask import Flask, redirect
import logging

app = Flask(__name__)


@app.route('/')
def redirect_to_komatbang():
    logging.info('redirecting to komatbang: https://www.instagram.com/komatbang/')
    return redirect('https://www.instagram.com/komatbang/')


@app.route('/health')
def health_check():
    return 'healthy'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
