import logging


logging.basicConfig(filename='log.txt',
                    level=logging.INFO,
                    filemode='w',
                    format='%(asctime)s - %(levelname)s: %(message)s')

logging.info('Write key X to 2')