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
            'stateless_z_scores': [{
                'Alpha': random.uniform(-1.0, 1.0),
                'Beta': random.uniform(-5.0, 5.0),
                'Gamma': random.uniform(-5.0, 5.0),
                'Delta': random.uniform(-5.0, 5.0),
                'Theta': random.uniform(-5.0, 5.0),
                'Sigma': random.uniform(-5.0, 5.0),
            }]
        }

    def generate_mock_event(self):
        return type('Event', (object,), {'message': self.generate_random_data()})

    def write_log_continuously(self):
        while True:
            data = self.generate_mock_event()
            logging.info(data.message)
            save_data(data)
            time.sleep(0.1)


