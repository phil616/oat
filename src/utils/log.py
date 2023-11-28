"""
    filename: utils/log.py
    ~~~~~~~~~~~~~~~~~~~~
    logger class for logging

    author: phil616
    date: 2023/11/28
    license: Apache License 2.0
"""

import logging
import os
from app_setting import config
class Logger:
    def __init__(self, log_name, log_file:os.PathLike=None,level=logging.DEBUG):
        """
        Constructor for logger class
        Args:
            log_name (str): Name of the logger
            log_file (str): Path to the log file
            level (int): Logging level
        """
        self.logger = logging.getLogger(log_name)
        self.logger.setLevel(level) 
        
        dir_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),config.LOG_PATH)

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        if log_file is None:
            log_file = os.path.join(dir_path, 'applog.log')
        else:
            log_file = os.path.join(dir_path, log_file)
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def get_logger(self):
        return self.logger
    
logger = Logger('syslog').get_logger()
