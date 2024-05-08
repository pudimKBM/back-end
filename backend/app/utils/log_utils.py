import logging

def setup_logger(name, log_file, level=logging.INFO):
    """Function to set up logging configuration"""
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    
    return logger