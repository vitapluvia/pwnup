from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

ns = {}
with open(path.join(here, 'pwnup/version.py'), encoding='utf-8') as fd:
    exec fd.read() in ns
version = ns['__version__']

setup(
    name='pwnup',
    version=version,
    description='A utility to scaffold out pwntools projects',
    author='vitapluvia',
    author_email='vitapluvia [at] gmail.com',
    url='https://github.com/vitapluvia/pwnup',
    license='MIT',
    classifiers=[
        'Topic :: Security',
        'Environment :: Console',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Intended Audience :: Developers',
        'Development Status :: 3 - Alpha'
    ],
    keywords='pwn security automation cli clients',
    packages=find_packages(exclude=['tests']),
    install_requires=['pyserial', 'pwntools'],
    entry_points={
        'console_scripts': [
            'pwnup=pwnup.pwnup:start',
        ],
    },
)
