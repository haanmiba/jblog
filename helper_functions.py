import os
import re
from datetime import datetime
from configparser import ConfigParser

def get_jekyll_blog_path(settings_file_name):
    """
    Gets the file path to the user's Jekyll blog.

    Parameters
    ----------
    settings_file_name : string
        name of the config settings file
    
    Returns
    -------
    string
        file path to the user's Jekyll blog
    """
    config_parser = ConfigParser()
    config_parser.read(settings_file_name)
    return config_parser['jekyll']['project_directory']


def create_url(title):
    """
    Creates a URL from a blog post.

    Parameters
    ----------
    title : string
        string that will converted into a URL
    
    Returns
    -------
    string
        URL representation of a string input
    """
    return '-'.join((re.sub('[^A-Za-z0-9_ ]+', '', title.strip().lower())).split(' '))


def get_current_date_time():
    """
    Get the current date and time.

    Returns
    -------
    tuple (string, string)
        A tuple containing the date and time
    """
    now = datetime.now()
    date = now.strftime('%Y-%m-%d')
    time = now.strftime('%H:%M:%S -4000')
    return date, time


def file_exists(filename):
    """
    Check if a file exists.

    Returns
    -------
    bool
        True if the file exists, False if it does not
    """
    return os.path.exists(filename)