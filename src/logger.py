import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('ALA')
hdlr = logging.FileHandler('./ALA.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s %(process)d')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)