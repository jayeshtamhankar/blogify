import os
import json

USER_DATA = 'data/user_data.json'
BLOG_DATA = 'data/blog_data.json'

def file_initialization(file_path):
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        with open(file_path, 'w') as data_file:
            json.dump([], data_file, indent=4)
        return True
    return False


def read_user_data():
    try:
        file_initialization(USER_DATA)
        with open(USER_DATA, 'r') as file:
            user_data = json.load(file)
            if not user_data:
                user_data = [{'users': []}]
            return user_data
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return [{'users': []}]

def write_user_data(data):
    try:
        file_initialization(USER_DATA)
        with open(USER_DATA, 'w') as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def read_blog_data():
    try:
        file_initialization(BLOG_DATA)
        with open(BLOG_DATA, 'r') as file:
            blog_data = json.load(file)
            if not blog_data:
                blog_data = [{'blogs': []}]
            return blog_data
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return [{'blogs': []}]

def write_blog_data(data):
    try:                        
        file_initialization(BLOG_DATA)
        with open(BLOG_DATA, 'w') as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
