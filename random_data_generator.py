import logging
import random
import time
import sys

class ContinuousLogger:
    def __init__(self, output='file'):
        self.configure_logging(output)
        
    def configure_logging(self, output):
        if output == 'console':
            logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                                format='%(asctime)s [INFO] %(message)s')
        else:
            logging.basicConfig(filename='continuous_logfile.log', level=logging.INFO,
                                format='%(asctime)s [INFO] %(message)s')
    
    def generate_random_data(self):
        return {
            'Delta': random.uniform(-5.0, 5.0),
            'Theta': random.uniform(-5.0, 5.0),
            'Alpha': random.uniform(-5.0, 5.0),
            'Sigma': random.uniform(-5.0, 5.0),
            'Beta': random.uniform(-5.0, 5.0),
            'Gamma': random.uniform(-5.0, 5.0),
        }

    def write_log_continuously(self):
        while True:
            data = [self.generate_random_data()]
            logging.info(data)
            time.sleep(1)

if __name__ == '__main__':
    # Ask user for output preference
    output_option = 'console'
    logger = ContinuousLogger(output_option)
    logger.write_log_continuously()
