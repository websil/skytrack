import os
import re

from setuptools import find_packages, setup

REGEXP = re.compile(r"^__version__\W*=\W*'([\d.abrc]+)'")


def read_version():
    init_py = os.path.join(os.path.dirname(__file__), 'app', '__init__.py')

    with open(init_py) as f:
        for line in f:
            match = REGEXP.match(line)
            if match is not None:
                return match.group(1)
        else:
            msg = f'Cannot find version in ${init_py}'
            raise RuntimeError(msg)


install_requires = [
    'aiohttp==3.6.2',
    'async-timeout==3.0.1',
    'aioredis==1.3.1',
    'aiohttp_security[session]',
    'aiohttp-session==2.9.0',
    'sqlalchemy',
    'envparse',
    'gunicorn',
    'ujson',
    'psycopg2'
]

setup(
    name='skytrack',
    version=read_version(),
    description='',
    platforms=['POSIX'],
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    zip_safe=False,
)
