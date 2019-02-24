import os
import re
import shutil
import fileinput
import subprocess
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
    time = now.strftime('%H:%M:%S')
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


def update_blog_post_yaml_header_date_time(file_path, new_date=datetime.now().strftime('%Y-%m-%d'), new_time=datetime.now().strftime('%H:%M:%S')):
    for line in fileinput.input(file_path, inplace=True):
        if line.startswith('date:'):
            print('date: {} {}'.format(new_date, new_time))
        else:
            print(line, end='')


def update_blog_post_filename_date_time(file_path, new_date=datetime.now().strftime('%Y-%m-%d')):
    base_filename = os.path.basename(file_path)
    file_dir_path = os.path.dirname(file_path)
    updated_filename = new_date + '-' + base_filename[11:]
    updated_file_path = file_dir_path + '/' + updated_filename
    os.rename(file_path, updated_file_path)
    return updated_file_path


def move_file(file_path, dest_folder):
    base_filename = os.path.basename(file_path)
    dest_file_path = dest_folder + '/' + base_filename
    shutil.move(file_path, dest_file_path)