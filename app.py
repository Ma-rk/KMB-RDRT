import json
import time
import uuid
import logging as lg
from logging.handlers import TimedRotatingFileHandler
from functools import wraps
from flask import Flask, redirect, request, g

app = Flask(__name__)


def setup_logger():
    logger = lg.getLogger()
    logger.setLevel(lg.INFO)

    log_file_handler = TimedRotatingFileHandler(
        './logs/KMB_app.log', when="midnight", interval=1, backupCount=30
    )
    log_file_handler.setFormatter(lg.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    ))

    console_handler = lg.StreamHandler()
    console_handler.setFormatter(lg.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    ))

    if logger.hasHandlers():
        logger.handlers.clear()

    logger.addHandler(log_file_handler)
    logger.addHandler(console_handler)


setup_logger()


def generate_request_id():
    """고유한 요청 ID를 생성합니다."""
    return str(uuid.uuid4())


def request_id_middleware():
    """각 요청에 고유 ID를 할당하는 미들웨어"""

    @wraps(request_id_middleware)
    def middleware():
        request_id = request.headers.get('X-Request-ID')
        if not request_id:
            request_id = generate_request_id()
        g.request_id = request_id
        return request_id

    return middleware


@app.before_request
def before_request():
    g.request_id = request_id_middleware()()


@app.route('/')
def redirect_to_komatbang():
    lg.info(f'[{g.request_id}] redirecting to komatbang: https://www.instagram.com/komatbang/')
    return redirect('https://www.instagram.com/komatbang/')


@app.route('/health-http')
def health_check_http():
    return 'healthy'


@app.teardown_request
def teardown_request(exception):
    lg.info(f'[{g.request_id}][teardown_request] request: {request}')
    lg.info(f'[{g.request_id}][teardown_request] request.path: {request.path}')
    lg.info(f'[{g.request_id}][teardown_request] request.url: {request.url}')
    headers_data = dict(request.headers)
    formatted_headers = json.dumps(headers_data, indent=4, separators=(",", ": "), ensure_ascii=False)
    lg.info(f'[{g.request_id}][teardown_request] Headers Data:\n{formatted_headers}')
