from setuptools import setup

setup(
    name='JekyllBlogPostCLI',
    version='1.0',
    py_modules=[
        'jekyll_blog_cli'
    ],
    install_requires=[
        'click',
    ],
    entry_points='''
        [console_scripts]
        jblog=jekyll_blog_cli:entry
    '''
)