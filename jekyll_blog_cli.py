import click
import os
import re
import helper_functions as hf
from config import Config


SETTINGS_FILE_PATH = os.path.dirname(os.path.realpath(__file__)) + '/settings.cfg'
JEKYLL_BLOG_PATH = hf.get_jekyll_blog_path(SETTINGS_FILE_PATH)

if JEKYLL_BLOG_PATH.endswith('/'):
    JEKYLL_BLOG_PATH = JEKYLL_BLOG_PATH[:-1]
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
def test(config):
    click.echo(os.path.realpath(__file__))

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
    if click.confirm('Do you wish to enter a preview for this blog post at this time?'):
        post_preview = click.prompt('Enter post preview', type=str)

    yaml_header = YAML_HEADER.format(title=post_title, date=post_date, time=post_time, categories=post_categories, preview=post_preview)
    dest_path = DRAFTS_PATH + '/{file_name}.markdown'.format(file_name=post_url)
    if hf.file_exists(dest_path):
        if click.confirm('`{file_name}` already exists. Do you want to overwrite it?'.format(file_name=dest_path)):
            if config.verbose:
                click.echo('Command completed. New blog post not created.')
            return
    
    try:
        with open(dest_path, 'w') as post_file:
            for line in yaml_header.split('\n'):
                post_file.write(line.strip() + '\n')
    except FileNotFoundError as e:
        click.echo(str(e))
        return
    
    if config.verbose:
        click.echo('New blog post created: `{file_name}`'.format(dest_path))


@entry.command()
@click.argument('filename', default=None, required=False)
@pass_config
def publish(config, filename):
    if config.verbose:
        click.echo('Publishing blog post...')

    while not filename:
        filename = click.prompt('Please enter the path to the blog post you wish to publish', type=str)

    if not filename.lower().endswith('.markdown'):
        click.echo('A Jekyll blog post must be a file that ends with `.markdown`')
        click.echo('`{filename}` was unable to be published'.format(filename=filename))
        return
    
    try:
        if config.verbose:
            click.echo('Updating blog post YAML header date and time...')
        hf.update_blog_post_yaml_header_date_time(filename)

        updated_file_path = hf.update_blog_post_filename_date_time(filename)

        if config.verbose and updated_file_path != filename:
            click.echo('Updated blog post filename to reflect new date.')
            click.echo('\tOld filename: {}'.format(os.path.basename(filename)))
            click.echo('\tNew filename: {}'.format(os.path.basename(updated_file_path)))

        if config.verbose:
            click.echo('Moving blog post to {posts_path}'.format(posts_path=POSTS_PATH))
        hf.move_file(updated_file_path, dest_folder=POSTS_PATH)
    except FileNotFoundError as e:
        click.echo(str(e))
        return

    if config.verbose:
        click.echo('Successfully published `{}`!'.format(updated_file_path))


@entry.command()
@click.argument('filename', default=None, required=False)
@pass_config
def unpublish(config, filename):
    if config.verbose:
        click.echo('Unpublishing blog post...')
    
    while not filename:
        filename = click.prompt('Please enter the path to the blog post you wish to publish', type=str)

    try:
        if config.verbose:
            click.echo('Moving blog post to `{drafts_path}`'.format(drafts_path=DRAFTS_PATH))
        hf.move_file(filename, DRAFTS_PATH)
    except FileNotFoundError as e:
        click.echo(str(e))
        return

    if config.verbose:
        click.echo('Successfully unpublished `{}`!'.format(os.path.basename(filename)))