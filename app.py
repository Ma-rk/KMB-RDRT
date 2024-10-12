import os
import json
import uuid
import logging as lg
from logging.handlers import TimedRotatingFileHandler
from functools import wraps
from flask import Flask, redirect, request, g
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.RequestLog import RequestLog

app = Flask(__name__)

app.config['RDS_KMB_ENDPOINT'] = os.environ['RDS_KMB_ENDPOINT']
app.config['RDS_KMB_PORT'] = os.environ['RDS_KMB_PORT']
app.config['RDS_KMB_ID'] = os.environ['RDS_KMB_ID']
app.config['RDS_KMB_PW'] = os.environ['RDS_KMB_PW']
app.config[
    'SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.environ['RDS_KMB_ID']}:{os.environ['RDS_KMB_PW']}@{os.environ['RDS_KMB_ENDPOINT']}:{os.environ['RDS_KMB_PORT']}/KMB"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


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

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
Session = sessionmaker(bind=engine)
session = Session()


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


def insert_request_items():
    header_items = RequestLog(request.path, request.url, request.headers)
    lg.info(header_items)
    session.add(header_items)
    session.commit()


def print_request_log():
    lg.info(f'[{g.request_id}][teardown_request] request: {request}')
    lg.info(f'[{g.request_id}][teardown_request] request.path: {request.path}')
    lg.info(f'[{g.request_id}][teardown_request] request.url: {request.url}')
    headers_data = dict(request.headers)
    formatted_headers = json.dumps(headers_data, indent=4, separators=(",", ": "), ensure_ascii=False)
    lg.info(f'[{g.request_id}][teardown_request] Headers Data:\n{formatted_headers}')


@app.teardown_request
def teardown_request(exception):
    print_request_log()
    insert_request_items()
