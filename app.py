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
    lg.info(f'request.headers: {request.headers}')
    lg.info(f'protocol: {request.headers.get("X-Forwarded-Proto", "http")}')

    # URL 쿼리 파라미터 (GET 요청)
    query_params = request.args.to_dict()

    # 폼 데이터 (POST 요청, enctype="application/x-www-form-urlencoded")
    form_data = request.form.to_dict()

    # JSON 데이터 (POST 요청, Content-Type: application/json)
    json_data = request.get_json() if request.is_json else {}

    # 헤더
    headers_data = dict(request.headers)

    # 쿠키
    cookies_data = request.cookies.to_dict()

    # 파일 (multipart/form-data)
    files_data = {file.filename: file for file in request.files.values()}

    # 모든 데이터를 합치기
    all_data = {
        'query_params': query_params,
        'form_data': form_data,
        'json_data': json_data,
        'headers_data': headers_data,
        'cookies_data': cookies_data,
        'files_data': list(files_data.keys())  # 파일 이름만 출력
    }

    lg.info(all_data)
    return redirect('https://www.instagram.com/komatbang/')


@app.route('/health-http')
def health_check_http():
    return 'healthy'
