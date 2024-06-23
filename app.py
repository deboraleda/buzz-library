from src import app, logger
from src import routes

if __name__ == '__main__':
    logger.info('Iniciando a aplicação em 0.0.0.0/8080')
    app.run(host='0.0.0.0', port=8080, debug=True)
