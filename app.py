from flask import Flask, redirect
import logging as lg
from logging.handlers import TimedRotatingFileHandler

app = Flask(__name__)


def setup_logger():
    logger = lg.getLogger()
    logger.setLevel(lg.INFO)  # 로그 레벨 설정

    # 로그 파일 핸들러 (컨테이너 외부의 ~/logs 경로로 설정)
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
    return redirect('https://www.instagram.com/komatbang/')


@app.route('/http')
def redirect_to_komatbang_http():
    lg.info('http!!! redirecting to komatbang: https://www.instagram.com/komatbang/')
    return redirect_to_komatbang()


@app.route('/http-www')
def redirect_to_komatbang_http_www():
    lg.info('http-www!!! redirecting to komatbang: https://www.instagram.com/komatbang/')
    return redirect_to_komatbang()


@app.route('/https')
def redirect_to_komatbang_https():
    lg.info('http!!! redirecting to komatbang: https://www.instagram.com/komatbang/')
    return redirect_to_komatbang()


@app.route('/https-www')
def redirect_to_komatbang_https_www():
    lg.info('https-www!!! redirecting to komatbang: https://www.instagram.com/komatbang/')
    return redirect_to_komatbang()


@app.route('/health-http')
def health_check_http():
    return 'healthy'
