import logging
from modules import logger

def main():
	logger_bugs.info("Hello world")


if __name__ == "__main__":
	logger.log_setup()
	logger_bugs = logging.getLogger("Bugs")
	main()
