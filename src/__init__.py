from flask import Flask
import os
import logging
from logging.handlers import RotatingFileHandler

log_directory = "log"
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
log_file_path = os.path.join(log_directory, 'logs.log')
handler = RotatingFileHandler(log_file_path, maxBytes=10000, backupCount=3)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.info("Configuração de logging inicializada.")

app = Flask(__name__)


