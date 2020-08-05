import logging
from modules import logger, client

def main():
	meta = client.Client().get_meta(type="album", id=990817)
	print(meta)


if __name__ == "__main__":
	logger.log_setup()
	logger_bugs = logging.getLogger("Bugs")
	main()
