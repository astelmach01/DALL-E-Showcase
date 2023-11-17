from dotenv import load_dotenv, find_dotenv
from pathlib import Path
import logging

APP_DIRECTORY = Path(__file__).parent

load_dotenv(find_dotenv())

logging.basicConfig(
    level=logging.INFO,  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(message)s",  # Format of the log messages
    datefmt="%Y-%m-%d %H:%M:%S",  # Date format
)
