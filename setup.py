from distutils.core import setup
import os

version = '0.5'
github_url = 'https://github.com/johnsyweb/python_sparse_list'
paj = 'Pete Johns'
paj_email = 'paj+pypi@johnsy.com'

setup(
    name='sparse_list',
    py_modules=['sparse_list'],
    version=version,
    description='A list where most (>95%) values will be None (or default)',
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
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
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
