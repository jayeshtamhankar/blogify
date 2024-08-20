import random
import string
import time
from datetime import datetime
from data import read_blog_data, read_user_data

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


def get_user_data(user_id=None, username=None):
    user_data = read_user_data()
    
    for user_container in user_data:
        for user in user_container['users']:
            if user['user_id'] == user_id:
                return user
            elif user['username'] == username:
                return user
    return None

def get_blog_data(blog_id=None):
    blog_data = read_blog_data ()
    
    if blog_id:
        for blog_container in blog_data:
            for blog in blog_container['blogs']:
                if blog['head']['blog_id'] == blog_id:
                    blog['head']['publish_data'] = datetime.strptime(blog['head']['publish_data'], '%d/%m/%y-%H:%M:%S').strftime("%d/%m/%Y")
                    return blog  # Return a single blog dictionary
    else:
        all_blogs = []
        for blog_container in blog_data:
            for blog in blog_container['blogs']:
                blog['head']['publish_data'] = datetime.strptime(blog['head']['publish_data'], '%d/%m/%y-%H:%M:%S').strftime("%d/%m/%Y")
                all_blogs.append(blog)
        return all_blogs
