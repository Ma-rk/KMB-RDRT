from flask import Flask, redirect, request
import logging as lg
from logging.handlers import TimedRotatingFileHandler

app = Flask(__name__)


def setup_logger():
    logger = lg.getLogger()
    logger.setLevel(lg.INFO)

    log_file_handler = TimedRotatingFileHandler(
        '/logs/KMB_app.log', when="midnight", interval=1, backupCount=30
    )
    log_file_handler.setFormatter(lg.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    ))

    logger.addHandler(log_file_handler)


setup_logger()


@app.route('/')
def redirect_to_komatbang():
    lg.info('redirecting to komatbang: https://www.instagram.com/komatbang/')
    lg.info(f'request: {request}')
    lg.info(f'request.path: {request.path}')
    lg.info(f'request.url: {request.url}')
    lg.info(f'request.headers: {request.headers}')
    lg.info(f'protocol: {request.headers.get("X-Forwarded-Proto", "http")}')
    return redirect('https://www.instagram.com/komatbang/')


@app.route('/health-http')
def health_check_http():
    return 'healthy'
