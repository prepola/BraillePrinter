from setuptools import setup

setup(name = 'brailleprinter',
    version = '0.1',
    url = 'https://github.com/prepola/brailleprinter/',
    license = 'MIT',
    author = 'prepola',
    author_email = 'jkh6912@gmail.com',
    zip_safe=False,
    setup_requires=[
        'nose>=1.0'
        ],
    test_suite='nose.collector'
    )
#    packages=find_packages(exclude=['tests']),
#    long_description=open('README.md').read(),