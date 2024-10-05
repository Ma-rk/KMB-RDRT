import json
from flask import Flask, redirect, request, jsonify
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

    if logger.hasHandlers():
        logger.handlers.clear()

    logger.addHandler(log_file_handler)


setup_logger()


@app.route('/')
def redirect_to_komatbang():
    lg.info('redirecting to komatbang: https://www.instagram.com/komatbang/')
    lg.info(f'request: {request}')
    lg.info(f'request.path: {request.path}')
    lg.info(f'request.url: {request.url}')

    # 헤더
    headers_data = dict(request.headers)

    lg.info('headers_data')
    lg.info(headers_data)

    formatted_headers = json.dumps(headers_data, indent=4, separators=(",", ": "), ensure_ascii=False)
    lg.info("Headers Data:\n%s", formatted_headers)

    return redirect('https://www.instagram.com/komatbang/')


@app.route('/health-http')
def health_check_http():
    return 'healthy'
