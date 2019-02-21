import os
import re
from datetime import datetime
from configparser import ConfigParser

def get_jekyll_blog_path():
    config_parser = ConfigParser()
    config_parser.read('settings.cfg')
    return config_parser['jekyll']['project_directory']


def create_url(title):
    return '-'.join((re.sub('[^A-Za-z0-9_ ]+', '', title.strip().lower())).split(' '))


def get_current_date_time():
    now = datetime.now()
    post_date = now.strftime('%Y-%m-%d')
    post_time = now.strftime('%H:%M:%S -4000')
    return post_date, post_time


def file_exists(filename):
    return os.path.exists(filename)