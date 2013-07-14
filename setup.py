from distutils.core import setup

version = '0.3'
github_url = 'https://github.com/johnsyweb/python_sparse_list'

setup(
    name='sparse_list',
    py_modules=['sparse_list'],
    version=version,
    description='A list where most (>95%) values will be None (or default)',
    author='Pete Johns',
    author_email='paj+pypi@johnsy.com',
    url=github_url,
    download_url='{}/tarball/{}'.format(github_url, version),
    keywords=['sparse', 'list', 'container', 'iterable'],
    classifiers=[],
)
