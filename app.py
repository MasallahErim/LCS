### File: src/presentation/api/app.py
from src.presentation.api import create_app
from src.infrastructure.logging.logger import setup_logging

setup_logging(level="DEBUG", log_to_file=True, logfile="/var/log/lounge.log")
app = create_app()

if __name__ == '__main__':
    # Running via "python app.py"
    app.run(host=app.config['API_HOST'], port=app.config['API_PORT'], debug=True)