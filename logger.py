import logging
import os
import datetime

today = datetime.datetime.now().strftime('%d-%b-%Y')

os.makedirs('logs', exist_ok=True)

name = 'facebook-crawler'

level = 10

logger = logging.getLogger(name)

handler = logging.StreamHandler()

formatter = logging.Formatter('[%(name)s] - %(message)s')

handler.setFormatter(formatter)

streamHandler = logging.FileHandler(f'logs/facebook-crawler-{today}.log')

formatter = logging.Formatter('%(asctime)s [%(name)s] - %(message)s', datefmt='%Y-%m-%d:%H:%M:%S')

streamHandler.setFormatter(formatter)

logger.addHandler(streamHandler)

logger.addHandler(handler)

logger.setLevel(level)

logger2 = logging.getLogger('post-texts')

handler = logging.FileHandler(f'logs/post-text-{today}.log')

handler.setLevel(10)

formatter = logging.Formatter('-' * 50 + '\n%(message)s')

handler.setFormatter(formatter)

logger2.addHandler(handler)