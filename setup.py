from setuptools import setup
import json
import os

version = '1.0'
github_url = 'https://github.com/johnsyweb/python_sparse_list'
paj = 'Pete Johns'
paj_email = 'paj+pypi@johnsy.com'

with open(os.path.join(os.path.dirname(__file__), 'ci', 'python_versions.json')) as f:
    python_versions = json.load(f)['python_versions']

python_classifiers = [
    'Programming Language :: Python :: {}'.format(version)
    for version in python_versions
]

setup(
    name='sparse_list',
    py_modules=['sparse_list'],
    version=version,
    description='A list where most values will be None (or some other default)',
    author=paj,
    author_email=paj_email,
    maintainer=paj,
    maintainer_email=paj_email,
    url=github_url,
    download_url='{}/tarball/{}'.format(github_url, version),
    keywords=['sparse', 'list', 'container', 'iterable'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ] + python_classifiers + [
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    long_description=(''.join(
        [open(f).read() for f in ('README.rst',) if os.path.isfile(f)]
    )),
    license='MIT'
)
