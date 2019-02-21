import click
import re
from datetime import datetime
from configparser import ConfigParser
import helper_functions as hf
from config import Config


SETTINGS_FILE_NAME = 'settings.cfg'
JEKYLL_BLOG_PATH = hf.get_jekyll_blog_path(SETTINGS_FILE_NAME)
DRAFTS_PATH = JEKYLL_BLOG_PATH + '/_drafts'
POSTS_PATH = JEKYLL_BLOG_PATH + '/_posts'
YAML_HEADER = '''---
layout: post
title: "{title}"
date: {date} {time}
categories: {categories}
preview: "{preview}"
---
'''

pass_config = click.make_pass_decorator(Config, ensure=True)


@click.group()
@click.option('--verbose', is_flag=True)
@pass_config
def entry(config, verbose):
    global JEKYLL_BLOG_PATH, DRAFTS_PATH, POSTS_PATH
    config.verbose = verbose
    if config.verbose:
        click.echo('We are now in verbose mode.')


@entry.command()
@pass_config
def new(config):
    if config.verbose:
        click.echo('Creating new blog post...')
    post_title = click.prompt('Title of post', type=str)
    post_url = hf.create_url(post_title)
    post_categories = re.sub(' +', ' ', click.prompt('Categories (each separated by a space)', type=str))

    post_date, post_time = hf.get_current_date_time()
    post_url = post_date + '-' + post_url

    post_preview = 'Enter post preview here.'
    if click.confirm('Do you wish to enter a preview for this blog post at this moment?'):
        post_preview = click.prompt('Enter post preview', type=str)

    yaml_header = YAML_HEADER.format(title=post_title, date=post_date, time=post_time, categories=post_categories, preview=post_preview)

    dest_path = DRAFTS_PATH + '/{file_name}.markdown'.format(file_name=post_url)
    if hf.file_exists(dest_path):
        if click.confirm('`{file_name}` already exists. Do you want to overwrite it?'.format(file_name=dest_path)):
            if config.verbose:
                click.echo('Command completed. New blog post not created.')
            return
    
    with open(dest_path, 'w') as post_file:
        for line in yaml_header.split('\n'):
            post_file.write(line.strip() + '\n')
    
    if config.verbose:
        click.echo('New blog post created: `{file_name}`'.format(dest_path))


@entry.command()
@click.argument('filename')
@pass_config
def publish(config):
    if config.verbose:
        click.echo('Publishing blog post...')
    


@entry.command()
@pass_config
def unpublish(config):
    if config.verbose:
        click.echo('Unpublishing blog post...')
