import random
import string
import time
from datetime import datetime

def generate_id():
    length = 8
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    time_stamp = str(int(time.time() * 1000))
    unique_id = random_string + time_stamp
    return unique_id

def time_stamp():
    current_time = datetime.now()
    stamp = current_time.strftime('%d/%m/%y-%H:%M:%S')
    return stamp